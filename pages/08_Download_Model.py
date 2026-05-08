import streamlit as st
import json
import pandas as pd
from utils.session_manager import init_session_state
from utils.helpers import sidebar_status
from utils.validators import validate_pipeline_exists
from utils.persistence import serialize_pipeline

st.set_page_config(page_title="Download Model", page_icon="💾", layout="wide")
init_session_state()
sidebar_status()

st.title("💾 Download Model")
st.markdown("Export the complete sklearn Pipeline (preprocessor + model) for deployment.")

if not validate_pipeline_exists():
    st.info("👈 Please complete **Train Model** first.")
    st.stop()

pipeline      = st.session_state["pipeline"]
model_name    = st.session_state.get("trained_model_name", "model")
task_type     = st.session_state.get("task_type", "")
feature_cols  = st.session_state.get("feature_cols", [])
target_col    = st.session_state.get("target_col", "")
model_results = st.session_state.get("model_results", {})
label_encoder = st.session_state.get("label_encoder")
preproc_cfg   = st.session_state.get("preprocessing_config", {})
cv_scores     = st.session_state.get("cv_scores")

# ── Summary ───────────────────────────────────────────────────────────────────
st.markdown("### 📦 Pipeline Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Model", model_name)
c2.metric("Task", task_type)
c3.metric("Features", len(feature_cols))
c4.metric("Target", target_col)

st.markdown("---")

# ── Metrics ───────────────────────────────────────────────────────────────────
metrics = model_results.get("metrics", {})
if metrics:
    st.markdown("### 📊 Test Set Metrics")
    metric_cols = st.columns(len(metrics))
    for col_ui, (name, val) in zip(metric_cols, metrics.items()):
        col_ui.metric(name, f"{val:.4f}" if isinstance(val, float) else str(val))

import numpy as np
if cv_scores is not None:
    scoring = "Accuracy" if task_type == "Classification" else "R²"
    st.info(
        f"CV {scoring}: {float(np.mean(cv_scores)):.4f} ± {float(np.std(cv_scores)):.4f}"
    )

st.markdown("---")

# ── Pipeline Details ──────────────────────────────────────────────────────────
st.markdown("### 🔧 Pipeline Components")
col_steps, col_cfg = st.columns(2)

with col_steps:
    st.markdown("""
**sklearn Pipeline:**
```
Pipeline
├── preprocessor (ColumnTransformer)
│   ├── num → SimpleImputer → Scaler
│   └── cat → SimpleImputer → Encoder
└── model
```
""")

with col_cfg:
    if preproc_cfg:
        st.markdown("**Preprocessing Config:**")
        cfg_display = {
            k: v for k, v in preproc_cfg.items()
            if k not in ("preprocessor",)
        }
        st.json(cfg_display)

st.markdown("---")

# ── Downloads ─────────────────────────────────────────────────────────────────
st.markdown("### ⬇️ Download")
dl1, dl2 = st.columns(2)

with dl1:
    st.markdown("#### 🤖 Pipeline (.joblib)")
    st.markdown(
        "Complete sklearn `Pipeline` with preprocessing + model. "
        "Ready to use with `joblib.load()`."
    )
    try:
        pipeline_bytes = serialize_pipeline(pipeline)
        safe_name = model_name.replace(" ", "_").lower()
        st.download_button(
            label="⬇️ Download Pipeline (.joblib)",
            data=pipeline_bytes,
            file_name=f"{safe_name}_pipeline.joblib",
            mime="application/octet-stream",
            type="primary",
            use_container_width=True,
        )
        st.caption(f"File size: {len(pipeline_bytes) / 1024:.1f} KB")
    except Exception as e:
        st.error(f"Serialization failed: {e}")

with dl2:
    st.markdown("#### 📄 Metadata (.json)")
    st.markdown(
        "Model configuration, test metrics, feature list, and class names."
    )
    metadata = {
        "model_name": model_name,
        "task_type": task_type,
        "target_col": target_col,
        "feature_cols": feature_cols,
        "test_metrics": {k: float(v) if isinstance(v, float) else v
                         for k, v in metrics.items()},
        "cv_scores": {
            "mean": round(float(np.mean(cv_scores)), 4),
            "std":  round(float(np.std(cv_scores)), 4),
        } if cv_scores is not None else None,
        "label_classes": list(label_encoder.classes_) if label_encoder else None,
        "preprocessing": {
            k: v for k, v in preproc_cfg.items()
            if k not in ("preprocessor",)
        },
    }
    metadata_json = json.dumps(metadata, indent=2, default=str)
    safe_name = model_name.replace(" ", "_").lower()
    st.download_button(
        label="⬇️ Download Metadata (.json)",
        data=metadata_json.encode("utf-8"),
        file_name=f"{safe_name}_metadata.json",
        mime="application/json",
        use_container_width=True,
    )

st.markdown("---")

# ── Usage Guide ───────────────────────────────────────────────────────────────
st.markdown("### 💡 How to Use the Downloaded Pipeline")
st.code("""
import joblib
import pandas as pd

# Load the complete pipeline
pipeline = joblib.load("your_model_pipeline.joblib")

# Create a DataFrame with the same feature columns used during training
new_data = pd.DataFrame({
    "feature_1": [value_1],
    "feature_2": [value_2],
    # ... one entry per feature column
})

# Predict — preprocessing happens automatically inside the pipeline
predictions = pipeline.predict(new_data)

# For classification: get class probabilities
probabilities = pipeline.predict_proba(new_data)

print("Prediction:", predictions[0])
print("Probabilities:", probabilities[0])
""", language="python")

st.warning(
    "⚠️ **Important:** Pass **raw, unprocessed** feature values to `pipeline.predict()`. "
    "The pipeline handles imputation, scaling, and encoding internally. "
    "Do NOT pre-process the data manually before prediction."
)

if feature_cols:
    st.markdown("#### Expected Feature Columns")
    feat_df = pd.DataFrame({
        "Column": feature_cols,
        "Index": list(range(len(feature_cols))),
    })
    st.dataframe(feat_df, use_container_width=True)
