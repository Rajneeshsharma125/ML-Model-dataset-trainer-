import streamlit as st
import pandas as pd
from utils.session_manager import init_session_state, reset_downstream
from utils.helpers import sidebar_status
from utils.validators import validate_dataframe
from utils.preprocessing import detect_column_types, build_preprocessor
from utils.training import split_data
from utils.config import (
    NUMERIC_IMPUTE_STRATEGIES, CAT_IMPUTE_STRATEGIES,
    SCALER_OPTIONS, ENCODER_OPTIONS, DEFAULT_TEST_SIZE,
)

st.set_page_config(page_title="Preprocessing", page_icon="⚙️", layout="wide")
init_session_state()
sidebar_status()

st.title("⚙️ Preprocessing")
st.markdown("Configure the sklearn Pipeline that transforms your data before training.")

df = st.session_state.get("df")
target_col = st.session_state.get("target_col")
feature_cols = st.session_state.get("feature_cols", [])
task_type = st.session_state.get("task_type")

if not validate_dataframe(df):
    st.info("👈 Please complete **Upload Data** first.")
    st.stop()

if not target_col or not feature_cols:
    st.warning("Please complete **Upload Data** configuration first.")
    st.stop()

numeric_cols, categorical_cols = detect_column_types(df, feature_cols)

# ── Column Summary ────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 🔢 Numeric Feature Columns")
    if numeric_cols:
        for c in numeric_cols:
            miss = int(df[c].isnull().sum())
            st.write(f"- `{c}` — {miss} missing")
    else:
        st.write("None")
with c2:
    st.markdown("#### 🔤 Categorical Feature Columns")
    if categorical_cols:
        for c in categorical_cols:
            miss = int(df[c].isnull().sum())
            nuniq = int(df[c].nunique())
            st.write(f"- `{c}` — {nuniq} unique, {miss} missing")
    else:
        st.write("None")

st.markdown("---")
st.markdown("### 🔢 Numeric Settings")
n1, n2 = st.columns(2)
with n1:
    numeric_impute = st.selectbox("Imputation Strategy", NUMERIC_IMPUTE_STRATEGIES, index=0,
                                  help="How to fill missing numeric values")
with n2:
    scaler = st.selectbox("Scaling Method", SCALER_OPTIONS, index=1,
                          help="Applied after imputation. StandardScaler recommended.")

st.markdown("### 🔤 Categorical Settings")
e1, e2 = st.columns(2)
with e1:
    cat_impute = st.selectbox("Imputation Strategy", CAT_IMPUTE_STRATEGIES, index=0,
                              key="cat_imp")
with e2:
    encoder = st.selectbox("Encoding Method", ENCODER_OPTIONS, index=0,
                           help="OneHotEncoder for tree models; OrdinalEncoder for others")

st.markdown("### ✂️ Train / Test Split")
s1, s2 = st.columns(2)
with s1:
    test_size = st.slider("Test Set Size", 0.10, 0.40, DEFAULT_TEST_SIZE, step=0.05,
                          help="Fraction of data reserved for testing")
with s2:
    st.info(
        f"Train: ~{int((1 - test_size) * len(df)):,} samples  |  "
        f"Test: ~{int(test_size * len(df)):,} samples"
    )
    if task_type == "Classification":
        st.caption("stratify=y applied automatically")

st.markdown("---")
if st.button("✅ Apply & Split Data", type="primary", use_container_width=True):
    with st.spinner("Building preprocessor and splitting data..."):
        try:
            X_train, X_test, y_train, y_test, label_encoder = split_data(
                df, feature_cols, target_col, task_type, test_size=test_size
            )
            preprocessor = build_preprocessor(
                numeric_cols=numeric_cols,
                categorical_cols=categorical_cols,
                numeric_impute=numeric_impute,
                scaler=scaler,
                cat_impute=cat_impute,
                encoder=encoder,
            )

            # Save — clear downstream model state
            reset_downstream("preprocessing")
            st.session_state["X_train"] = X_train
            st.session_state["X_test"]  = X_test
            st.session_state["y_train"] = y_train
            st.session_state["y_test"]  = y_test
            st.session_state["label_encoder"] = label_encoder
            st.session_state["preprocessor"] = preprocessor
            st.session_state["preprocessing_config"] = {
                "numeric_cols":   numeric_cols,
                "categorical_cols": categorical_cols,
                "numeric_impute": numeric_impute,
                "scaler":         scaler,
                "cat_impute":     cat_impute,
                "encoder":        encoder,
                "test_size":      test_size,
            }

            st.success("✅ Preprocessing pipeline built and data split successfully!")
            m1, m2, m3 = st.columns(3)
            m1.metric("Train Samples", X_train.shape[0])
            m2.metric("Test Samples",  X_test.shape[0])
            m3.metric("Features",      X_train.shape[1])
            if label_encoder is not None:
                st.info(f"Target encoded — Classes: {list(label_encoder.classes_)}")

        except Exception as e:
            st.error(f"Error during preprocessing: {e}")
            import traceback
            st.code(traceback.format_exc())

# ── Status ────────────────────────────────────────────────────────────────────
cfg = st.session_state.get("preprocessing_config", {})
if cfg:
    st.markdown("---")
    st.markdown("#### ✅ Active Configuration")
    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"Num Impute: **{cfg.get('numeric_impute')}**")
    c2.info(f"Scaler: **{cfg.get('scaler')}**")
    c3.info(f"Cat Impute: **{cfg.get('cat_impute')}**")
    c4.info(f"Encoder: **{cfg.get('encoder')}**")

    X_train = st.session_state.get("X_train")
    if X_train is not None:
        st.markdown("#### 🔍 Training Data Preview (first 10 rows)")
        st.dataframe(X_train.head(10), use_container_width=True)
