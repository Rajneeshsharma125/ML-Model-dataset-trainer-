import streamlit as st
from utils.session_manager import init_session_state
from utils.helpers import sidebar_status
from utils.config import APP_TITLE, APP_ICON

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
sidebar_status()

# ── Hero ─────────────────────────────────────────────────────────────────────
st.title(f"{APP_ICON} {APP_TITLE}")
st.markdown(
    "**An end-to-end Machine Learning platform — upload your data, "
    "preprocess, explore, train, evaluate, compare, predict, and download your model.**"
)
st.markdown("---")

# ── Workflow Cards ────────────────────────────────────────────────────────────
steps = [
    ("📁", "Upload Data",      "CSV / XLSX upload, preview, missing value report, duplicate removal."),
    ("⚙️", "Preprocessing",    "Configure imputation, scaling, encoding. Split train/test with no data leakage."),
    ("📊", "EDA",              "Histograms, box plots, scatter plots, heatmaps, target analysis."),
    ("🤖", "Train Model",      "Choose algorithm, tune hyperparameters, run cross-validation."),
    ("📈", "Evaluate",         "Confusion matrix, ROC curve, feature importance, full metrics."),
    ("⚖️", "Compare Models",   "Benchmark all algorithms side-by-side with radar chart."),
    ("🔮", "Predict",          "Single sample prediction or batch CSV upload prediction."),
    ("💾", "Download Model",   "Export complete sklearn Pipeline (.joblib) + metadata (.json)."),
]

cols = st.columns(4)
for idx, (icon, title, desc) in enumerate(steps):
    with cols[idx % 4]:
        st.info(f"**{icon} {title}**\n\n{desc}")

st.markdown("---")

# ── Quick Start ───────────────────────────────────────────────────────────────
st.markdown("### 🚀 Quick Start")
st.markdown(
    "1. Navigate to **Upload Data** in the sidebar and load your CSV or Excel file.\n"
    "2. Select your **target column** and feature columns.\n"
    "3. Configure **Preprocessing** (imputation, scaling, encoding).\n"
    "4. Explore your data in **EDA**.\n"
    "5. **Train** a model and **Evaluate** performance.\n"
    "6. **Compare** multiple models to find the best one.\n"
    "7. Use **Predict** for new data, then **Download** the pipeline."
)

st.markdown("---")

c1, c2 = st.columns(2)
with c1:
    st.markdown("### Classification Models")
    for m in ["Logistic Regression", "Decision Tree", "Random Forest",
              "K-Nearest Neighbors", "Support Vector Machine"]:
        st.markdown(f"- {m}")

with c2:
    st.markdown("### Regression Models")
    for m in ["Linear Regression", "Random Forest Regressor"]:
        st.markdown(f"- {m}")

st.markdown("---")
st.caption(
    "random_state=42 · stratify=y for classification · "
    "Train/test split BEFORE preprocessing · "
    "Complete pipeline saved with joblib"
)
