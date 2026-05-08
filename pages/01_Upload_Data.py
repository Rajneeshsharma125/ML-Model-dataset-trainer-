import streamlit as st
import pandas as pd
from utils.session_manager import init_session_state, reset_downstream
from utils.helpers import load_uploaded_file, sidebar_status
from utils.validators import validate_file_extension, validate_dataframe, validate_target, validate_features
from utils.preprocessing import auto_detect_task, get_missing_report
from utils.config import APP_ICON

st.set_page_config(page_title="Upload Data", page_icon="📁", layout="wide")
init_session_state()
sidebar_status()

st.title("📁 Upload Data")
st.markdown("Upload your CSV or Excel dataset to begin.")

# ── File Upload ───────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Choose a file (CSV or XLSX)",
    type=["csv", "xlsx", "xls"],
    help="First row must contain column headers.",
)

if uploaded is not None:
    if not validate_file_extension(uploaded.name):
        st.stop()

    with st.spinner("Loading file..."):
        try:
            df_raw = load_uploaded_file(uploaded)
        except Exception as e:
            st.error(f"Failed to read file: {e}")
            st.stop()

    if not validate_dataframe(df_raw):
        st.stop()

    st.success(f"✅ **{uploaded.name}** loaded — {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_prev, tab_miss, tab_dup, tab_stats = st.tabs([
        "🔍 Preview", "📉 Missing Values", "🔁 Duplicates", "📊 Statistics"
    ])

    with tab_prev:
        st.dataframe(df_raw.head(50), use_container_width=True)

    with tab_miss:
        miss_df = get_missing_report(df_raw)
        has_miss = miss_df[miss_df["Missing Count"] > 0]
        if has_miss.empty:
            st.success("✅ No missing values detected.")
        else:
            st.warning(f"⚠️ {len(has_miss)} column(s) have missing values.")
            st.dataframe(has_miss, use_container_width=True)
            import plotly.express as px
            hm = has_miss.reset_index()
            hm.columns = ["Column", "Missing Count", "Missing %", "Dtype"]
            st.plotly_chart(
                px.bar(hm, x="Column", y="Missing %", color="Missing %",
                       color_continuous_scale="Reds", title="Missing % per Column"),
                use_container_width=True,
            )

    with tab_dup:
        n_dup = int(df_raw.duplicated().sum())
        if n_dup == 0:
            st.success("✅ No duplicate rows found.")
        else:
            st.warning(f"⚠️ {n_dup} duplicate rows detected.")
            if st.button("🗑️ Remove Duplicates"):
                df_raw = df_raw.drop_duplicates().reset_index(drop=True)
                st.success(f"Removed duplicates. New shape: {df_raw.shape[0]} rows.")

    with tab_stats:
        st.dataframe(df_raw.describe(include="all").T, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚙️ Configure Target & Features")

    all_cols = df_raw.columns.tolist()

    col_left, col_right = st.columns(2)
    with col_left:
        target_col = st.selectbox(
            "🎯 Target Column (what to predict)",
            options=all_cols,
            index=len(all_cols) - 1,
        )
    with col_right:
        detected_task = auto_detect_task(df_raw, target_col)
        task_type = st.radio(
            "📋 Task Type",
            options=["Classification", "Regression"],
            index=0 if detected_task == "Classification" else 1,
            horizontal=True,
        )
        st.caption(f"Auto-detected: **{detected_task}**")

    feature_candidates = [c for c in all_cols if c != target_col]
    feature_cols = st.multiselect(
        "📌 Feature Columns",
        options=feature_candidates,
        default=feature_candidates,
    )

    st.markdown("---")
    if st.button("✅ Confirm & Save", type="primary", use_container_width=True):
        if not validate_target(df_raw, target_col):
            st.stop()
        if not validate_features(feature_cols):
            st.stop()

        reset_downstream("data")
        st.session_state["df_raw"] = df_raw
        st.session_state["df"] = df_raw.copy()
        st.session_state["filename"] = uploaded.name
        st.session_state["target_col"] = target_col
        st.session_state["feature_cols"] = feature_cols
        st.session_state["task_type"] = task_type
        st.success("✅ Configuration saved! Proceed to **Preprocessing**.")
        st.balloons()

# ── Current Config Banner ─────────────────────────────────────────────────────
if st.session_state.get("df") is not None:
    st.markdown("---")
    st.markdown("#### 📌 Current Configuration")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("File", st.session_state.get("filename", "—"))
    b2.metric("Target", st.session_state.get("target_col", "—"))
    b3.metric("Features", len(st.session_state.get("feature_cols", [])))
    b4.metric("Task", st.session_state.get("task_type", "—"))

    if st.button("🗑️ Clear All & Start Over", type="secondary"):
        reset_downstream("data")
        st.rerun()
