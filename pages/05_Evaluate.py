import streamlit as st
import numpy as np
import pandas as pd
from utils.session_manager import init_session_state
from utils.helpers import sidebar_status, metric_cards
from utils.validators import validate_pipeline_exists
from utils.plots import (
    fig_confusion_matrix, fig_roc_curve, fig_feature_importance,
    fig_actual_vs_predicted, fig_residuals,
)

st.set_page_config(page_title="Evaluate", page_icon="📈", layout="wide")
init_session_state()
sidebar_status()

st.title("📈 Model Evaluation")

if not validate_pipeline_exists():
    st.info("👈 Please complete **Train Model** first.")
    st.stop()

pipeline     = st.session_state["pipeline"]
model_name   = st.session_state.get("trained_model_name", "Unknown")
task_type    = st.session_state.get("task_type")
model_results= st.session_state.get("model_results", {})
cv_scores    = st.session_state.get("cv_scores")
label_encoder= st.session_state.get("label_encoder")

st.markdown(f"### Model: **{model_name}** | Task: **{task_type}**")
st.markdown("---")

metrics = model_results.get("metrics", {})
metric_cards(metrics)

if cv_scores is not None:
    scoring = "Accuracy" if task_type == "Classification" else "R²"
    st.info(
        f"**Cross-Validation {scoring}:** "
        f"{float(np.mean(cv_scores)):.4f} ± {float(np.std(cv_scores)):.4f}"
    )

st.markdown("---")

if task_type == "Classification":
    tab_cm, tab_roc, tab_report, tab_fi = st.tabs([
        "🟦 Confusion Matrix", "📉 ROC Curve",
        "📝 Classification Report", "🔑 Feature Importance",
    ])

    with tab_cm:
        cm = model_results.get("cm")
        class_names = model_results.get("class_names")
        if cm is not None:
            col_fig, col_tbl = st.columns([1, 1])
            with col_fig:
                st.pyplot(fig_confusion_matrix(cm, class_names))
            with col_tbl:
                labels = class_names if class_names else list(range(cm.shape[0]))
                cm_df = pd.DataFrame(
                    cm,
                    index=[f"Actual: {l}" for l in labels],
                    columns=[f"Pred: {l}" for l in labels],
                )
                st.markdown("#### Values")
                st.dataframe(cm_df, use_container_width=True)

                # Per-class accuracy
                per_class = {str(labels[i]): round(cm[i, i] / cm[i].sum(), 4)
                             for i in range(len(labels)) if cm[i].sum() > 0}
                st.markdown("#### Per-Class Recall")
                st.dataframe(
                    pd.DataFrame(per_class, index=["Recall"]).T.reset_index()
                      .rename(columns={"index": "Class"}),
                    use_container_width=True,
                )

    with tab_roc:
        fpr_tpr = model_results.get("fpr_tpr")
        roc_auc = metrics.get("ROC-AUC")
        if fpr_tpr is not None and roc_auc is not None:
            fpr, tpr = fpr_tpr
            st.pyplot(fig_roc_curve(fpr, tpr, roc_auc))
        else:
            st.info(
                "ROC curve is available for binary classification with "
                "probability-supporting models (all models here support it)."
            )

    with tab_report:
        report = model_results.get("report", "")
        if report:
            st.code(report, language="text")

    with tab_fi:
        fi_fig = fig_feature_importance(pipeline)
        if fi_fig:
            st.plotly_chart(fi_fig, use_container_width=True)
        else:
            st.info("Feature importance not available for this model.")

else:  # Regression
    y_pred = model_results.get("y_pred")
    y_test = st.session_state.get("y_test")

    tab_avp, tab_res, tab_fi = st.tabs([
        "📉 Actual vs Predicted", "📊 Residuals", "🔑 Feature Importance",
    ])

    with tab_avp:
        if y_pred is not None and y_test is not None:
            st.plotly_chart(fig_actual_vs_predicted(y_test, y_pred), use_container_width=True)

    with tab_res:
        if y_pred is not None and y_test is not None:
            st.plotly_chart(fig_residuals(y_test, y_pred), use_container_width=True)

            residuals = np.array(y_test) - np.array(y_pred)
            rc1, rc2 = st.columns(2)
            rc1.metric("Mean Residual", f"{float(np.mean(residuals)):.4f}")
            rc2.metric("Std Residual",  f"{float(np.std(residuals)):.4f}")

    with tab_fi:
        fi_fig = fig_feature_importance(pipeline)
        if fi_fig:
            st.plotly_chart(fi_fig, use_container_width=True)
        else:
            st.info("Feature importance not available for Linear Regression.")
