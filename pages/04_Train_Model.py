import streamlit as st
import numpy as np
from utils.session_manager import init_session_state, reset_downstream
from utils.helpers import sidebar_status, metric_cards
from utils.validators import validate_dataframe, validate_splits_exist
from utils.model_factory import (
    classifier_param_widgets, regressor_param_widgets, build_pipeline,
)
from utils.training import train_pipeline, run_cross_validation
from utils.evaluation import evaluate_classifier, evaluate_regressor
from utils.plots import fig_feature_importance
from utils.config import CLASSIFICATION_MODELS, REGRESSION_MODELS

st.set_page_config(page_title="Train Model", page_icon="🤖", layout="wide")
init_session_state()
sidebar_status()

st.title("🤖 Train Model")
st.markdown("Select an algorithm, tune hyperparameters, and train the complete sklearn Pipeline.")

df = st.session_state.get("df")
task_type = st.session_state.get("task_type")
X_train = st.session_state.get("X_train")
X_test  = st.session_state.get("X_test")
y_train = st.session_state.get("y_train")
y_test  = st.session_state.get("y_test")
label_encoder = st.session_state.get("label_encoder")
preprocessor = st.session_state.get("preprocessor")

if not validate_dataframe(df):
    st.info("👈 Please complete **Upload Data** first.")
    st.stop()
if not validate_splits_exist():
    st.info("👈 Please complete **Preprocessing** first.")
    st.stop()

model_list = CLASSIFICATION_MODELS if task_type == "Classification" else REGRESSION_MODELS
model_name = st.selectbox("🤖 Select Algorithm", model_list)

with st.expander("⚙️ Hyperparameters", expanded=True):
    if task_type == "Classification":
        model_params = classifier_param_widgets(model_name, st)
    else:
        model_params = regressor_param_widgets(model_name, st)

cv_folds = st.slider("Cross-Validation Folds", 2, 10, 5, key="cv_folds")

st.markdown("---")
if st.button("🚀 Train", type="primary", use_container_width=True):
    with st.spinner(f"Training {model_name}..."):
        try:
            pipeline = train_pipeline(
                X_train, y_train,
                preprocessor=preprocessor,
                model_name=model_name,
                task_type=task_type,
                model_params=model_params,
            )

            if task_type == "Classification":
                metrics, cm, fpr_tpr, class_names, report = evaluate_classifier(
                    pipeline, X_test, y_test, label_encoder
                )
                model_results = dict(
                    metrics=metrics, cm=cm, fpr_tpr=fpr_tpr,
                    class_names=class_names, report=report,
                )
            else:
                metrics, y_pred = evaluate_regressor(pipeline, X_test, y_test)
                model_results = dict(metrics=metrics, y_pred=y_pred)

            cv_scores = run_cross_validation(pipeline, X_train, y_train, task_type, cv=cv_folds)

            reset_downstream("training")
            st.session_state["pipeline"]           = pipeline
            st.session_state["trained_model_name"] = model_name
            st.session_state["model_results"]      = model_results
            st.session_state["cv_scores"]          = cv_scores

            st.success(f"✅ **{model_name}** trained successfully!")

        except Exception as e:
            st.error(f"Training failed: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

# ── Show results if current model matches ─────────────────────────────────────
if (st.session_state.get("trained_model_name") == model_name
        and st.session_state.get("model_results")):

    results = st.session_state["model_results"]
    cv_scores = st.session_state.get("cv_scores")
    pipeline = st.session_state["pipeline"]

    st.markdown("---")
    st.markdown("### 📊 Results")
    metric_cards(results["metrics"])

    if cv_scores is not None:
        cv_mean = float(np.mean(cv_scores))
        cv_std  = float(np.std(cv_scores))
        scoring = "Accuracy" if task_type == "Classification" else "R²"
        st.info(
            f"**{cv_folds}-Fold CV {scoring}:** "
            f"{cv_mean:.4f} ± {cv_std:.4f}  "
            f"(min={float(np.min(cv_scores)):.4f}, max={float(np.max(cv_scores)):.4f})"
        )

    feat_fig = fig_feature_importance(pipeline)
    if feat_fig:
        st.markdown("#### 🔑 Feature Importance")
        st.plotly_chart(feat_fig, use_container_width=True)

    st.markdown("#### ➡️ Next Steps")
    st.info("Go to **Evaluate** for detailed metrics, confusion matrix, and ROC curve.")
