import streamlit as st
import pandas as pd
from utils.session_manager import init_session_state, reset_downstream
from utils.helpers import sidebar_status, df_to_csv_bytes
from utils.validators import validate_dataframe, validate_splits_exist
from utils.model_factory import get_classifier, get_regressor, build_pipeline
from utils.evaluation import bulk_compare_classifiers, bulk_compare_regressors
from utils.plots import fig_model_comparison, fig_radar
from utils.config import CLASSIFICATION_MODELS, REGRESSION_MODELS

st.set_page_config(page_title="Compare Models", page_icon="⚖️", layout="wide")
init_session_state()
sidebar_status()

st.title("⚖️ Compare Models")
st.markdown("Train and benchmark all algorithms on your dataset simultaneously.")

df = st.session_state.get("df")
task_type    = st.session_state.get("task_type")
X_train      = st.session_state.get("X_train")
X_test       = st.session_state.get("X_test")
y_train      = st.session_state.get("y_train")
y_test       = st.session_state.get("y_test")
preprocessor = st.session_state.get("preprocessor")

if not validate_dataframe(df):
    st.info("👈 Please complete **Upload Data** first.")
    st.stop()
if not validate_splits_exist():
    st.info("👈 Please complete **Preprocessing** first.")
    st.stop()

model_list = CLASSIFICATION_MODELS if task_type == "Classification" else REGRESSION_MODELS
selected = st.multiselect(
    "Select Models to Compare",
    options=model_list,
    default=model_list,
)

if not selected:
    st.warning("Select at least one model to compare.")
    st.stop()

if st.button("🚀 Run Comparison", type="primary", use_container_width=True):
    with st.spinner("Training and evaluating all models..."):
        try:
            pipelines = {}
            for name in selected:
                try:
                    model = (get_classifier(name) if task_type == "Classification"
                             else get_regressor(name))
                    pipelines[name] = build_pipeline(preprocessor, model)
                except Exception as e:
                    st.warning(f"Skipping {name}: {e}")

            if task_type == "Classification":
                compare_df = bulk_compare_classifiers(pipelines, X_train, X_test, y_train, y_test)
            else:
                compare_df = bulk_compare_regressors(pipelines, X_train, X_test, y_train, y_test)

            reset_downstream("compare")
            st.session_state["compare_df"] = compare_df
            st.success("✅ Comparison complete!")

        except Exception as e:
            st.error(f"Comparison failed: {e}")
            import traceback
            st.code(traceback.format_exc())

compare_df = st.session_state.get("compare_df")
if compare_df is not None and not compare_df.empty:
    st.markdown("---")
    st.markdown("### 📊 Results Table")

    metric_cols = [c for c in compare_df.columns if c not in ("Model", "Error")]
    valid_metrics = [c for c in metric_cols if c in compare_df.columns
                     and compare_df[c].notna().any()]

    # Highlight best per column
    def highlight_best(s):
        is_max = s == s.max()
        return ["background-color: #d4edda; font-weight: bold" if v else "" for v in is_max]

    try:
        styled = compare_df.style.apply(highlight_best, subset=valid_metrics)
        st.dataframe(styled, use_container_width=True)
    except Exception:
        st.dataframe(compare_df, use_container_width=True)

    # Chart
    if valid_metrics:
        tab_bar, tab_radar = st.tabs(["📊 Bar Chart", "🕸️ Radar Chart"])

        with tab_bar:
            chart_metric = st.selectbox("Metric", valid_metrics, key="cmp_metric")
            st.plotly_chart(fig_model_comparison(compare_df, chart_metric), use_container_width=True)

        with tab_radar:
            radar_metrics = [m for m in valid_metrics if compare_df[m].between(0, 1).all()]
            if len(radar_metrics) >= 2:
                st.plotly_chart(fig_radar(compare_df, radar_metrics), use_container_width=True)
            else:
                st.info("Radar chart requires metrics in [0, 1] range (e.g., Accuracy, F1 Score).")

    # Best model
    if valid_metrics:
        primary = valid_metrics[0]
        try:
            best_idx = compare_df[primary].idxmax()
            best_row = compare_df.loc[best_idx]
            st.success(
                f"🏆 Best by **{primary}**: **{best_row['Model']}** — {best_row[primary]:.4f}"
            )
        except Exception:
            pass

    # Download
    csv_bytes = df_to_csv_bytes(compare_df)
    st.download_button(
        "⬇️ Download Comparison CSV",
        data=csv_bytes,
        file_name="model_comparison.csv",
        mime="text/csv",
    )
