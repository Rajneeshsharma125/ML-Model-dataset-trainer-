import streamlit as st
import pandas as pd
import numpy as np
import io
from utils.session_manager import init_session_state
from utils.helpers import sidebar_status, df_to_csv_bytes
from utils.validators import validate_pipeline_exists

st.set_page_config(page_title="Predict", page_icon="🔮", layout="wide")
init_session_state()
sidebar_status()

st.title("🔮 Predict")
st.markdown("Use the trained pipeline to make predictions on new data.")

if not validate_pipeline_exists():
    st.info("👈 Please complete **Train Model** first.")
    st.stop()

pipeline      = st.session_state["pipeline"]
model_name    = st.session_state.get("trained_model_name", "Model")
task_type     = st.session_state.get("task_type")
feature_cols  = st.session_state.get("feature_cols", [])
label_encoder = st.session_state.get("label_encoder")
df            = st.session_state.get("df")

st.info(f"**Active Model:** {model_name} | **Task:** {task_type} | **Features:** {len(feature_cols)}")

tab_single, tab_batch = st.tabs(["🔢 Single Prediction", "📦 Batch Prediction"])

# ── Single Prediction ─────────────────────────────────────────────────────────
with tab_single:
    st.markdown("### Enter Feature Values")
    if df is None or not feature_cols:
        st.warning("Dataset or features not configured.")
        st.stop()

    input_data = {}
    n_per_row = 3
    groups = [feature_cols[i:i+n_per_row] for i in range(0, len(feature_cols), n_per_row)]

    for grp in groups:
        cols_ui = st.columns(len(grp))
        for col_ui, feat in zip(cols_ui, grp):
            with col_ui:
                if pd.api.types.is_numeric_dtype(df[feat]):
                    col_min  = float(df[feat].min())
                    col_max  = float(df[feat].max())
                    col_mean = float(df[feat].mean())
                    input_data[feat] = st.number_input(
                        feat, min_value=col_min, max_value=col_max,
                        value=col_mean, key=f"sp_{feat}",
                        help=f"Range: [{col_min:.2f}, {col_max:.2f}]",
                    )
                else:
                    unique_vals = df[feat].dropna().unique().tolist()
                    input_data[feat] = st.selectbox(feat, options=unique_vals, key=f"sp_{feat}")

    st.markdown("---")
    if st.button("🔮 Predict", type="primary"):
        try:
            input_df = pd.DataFrame([input_data])
            raw_pred = pipeline.predict(input_df)[0]

            display_pred = raw_pred
            if label_encoder is not None:
                try:
                    display_pred = label_encoder.inverse_transform([int(raw_pred)])[0]
                except Exception:
                    pass

            st.success(f"### 🎯 Prediction: **{display_pred}**")

            if task_type == "Classification":
                try:
                    proba = pipeline.predict_proba(input_df)[0]
                    classes = (list(label_encoder.classes_) if label_encoder is not None
                               else list(range(len(proba))))
                    proba_df = pd.DataFrame({
                        "Class": classes,
                        "Probability": [round(float(p), 4) for p in proba],
                    }).sort_values("Probability", ascending=False)

                    st.markdown("#### Class Probabilities")
                    col_tbl, col_bar = st.columns(2)
                    with col_tbl:
                        st.dataframe(
                            proba_df.style.format({"Probability": "{:.4f}"}),
                            use_container_width=True,
                        )
                    with col_bar:
                        import plotly.express as px
                        fig_p = px.bar(
                            proba_df, x="Class", y="Probability",
                            color="Probability", color_continuous_scale="Blues",
                            title="Probability per Class",
                        )
                        st.plotly_chart(fig_p, use_container_width=True)
                except Exception:
                    pass

        except Exception as e:
            st.error(f"Prediction failed: {e}")
            import traceback
            st.code(traceback.format_exc())

# ── Batch Prediction ──────────────────────────────────────────────────────────
with tab_batch:
    st.markdown("### Upload a File for Batch Prediction")
    st.markdown(
        f"The file must contain these columns: "
        f"`{', '.join(feature_cols)}`"
    )

    batch_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        key="batch_upload",
    )

    if batch_file is not None:
        try:
            raw = batch_file.read()
            ext = batch_file.name.rsplit(".", 1)[-1].lower()
            if ext == "csv":
                batch_df = pd.read_csv(io.BytesIO(raw))
            else:
                batch_df = pd.read_excel(io.BytesIO(raw))

            st.markdown(f"Loaded **{batch_df.shape[0]:,}** rows × **{batch_df.shape[1]}** columns")
            st.dataframe(batch_df.head(5), use_container_width=True)

            missing_cols = [c for c in feature_cols if c not in batch_df.columns]
            if missing_cols:
                st.error(f"Missing columns: `{', '.join(missing_cols)}`")
            else:
                if st.button("🔮 Run Batch Prediction", type="primary"):
                    with st.spinner(f"Predicting {batch_df.shape[0]} rows..."):
                        try:
                            X_batch = batch_df[feature_cols].copy()
                            preds = pipeline.predict(X_batch)

                            if label_encoder is not None:
                                try:
                                    preds = label_encoder.inverse_transform(preds.astype(int))
                                except Exception:
                                    pass

                            result_df = batch_df.copy()
                            result_df["Prediction"] = preds

                            if task_type == "Classification":
                                try:
                                    proba_arr = pipeline.predict_proba(X_batch)
                                    classes = (list(label_encoder.classes_) if label_encoder
                                               else list(range(proba_arr.shape[1])))
                                    for i, cls in enumerate(classes):
                                        result_df[f"Prob_{cls}"] = np.round(proba_arr[:, i], 4)
                                except Exception:
                                    pass

                            st.success(f"✅ Predicted **{len(result_df):,}** rows.")
                            st.dataframe(result_df.head(20), use_container_width=True)

                            csv_bytes = df_to_csv_bytes(result_df)
                            st.download_button(
                                "⬇️ Download Predictions CSV",
                                data=csv_bytes,
                                file_name="batch_predictions.csv",
                                mime="text/csv",
                            )

                            # Summary
                            if task_type == "Classification":
                                vc = pd.Series(preds).value_counts().reset_index()
                                vc.columns = ["Prediction", "Count"]
                                st.markdown("#### Prediction Distribution")
                                import plotly.express as px
                                st.plotly_chart(
                                    px.bar(vc, x="Prediction", y="Count",
                                           title="Batch Prediction Distribution"),
                                    use_container_width=True,
                                )

                        except Exception as e:
                            st.error(f"Batch prediction failed: {e}")
                            import traceback
                            st.code(traceback.format_exc())

        except Exception as e:
            st.error(f"Failed to read file: {e}")
