import pandas as pd
import streamlit as st


def validate_file_extension(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ("csv", "xlsx", "xls"):
        st.error(f"Unsupported file type '.{ext}'. Please upload a CSV or Excel file.")
        return False
    return True


def validate_dataframe(df) -> bool:
    if df is None:
        st.warning("No dataset loaded. Please go to **Upload Data** first.")
        return False
    if df.empty:
        st.error("The dataset is empty.")
        return False
    if df.shape[1] < 2:
        st.error("Dataset must have at least 2 columns.")
        return False
    return True


def validate_target(df: pd.DataFrame, target: str) -> bool:
    if not target:
        st.warning("Please select a target column.")
        return False
    if target not in df.columns:
        st.error(f"Target column '{target}' not found.")
        return False
    if df[target].nunique() < 2:
        st.error("Target column must have at least 2 unique values.")
        return False
    return True


def validate_features(features: list) -> bool:
    if not features:
        st.warning("Please select at least one feature column.")
        return False
    return True


def validate_splits_exist() -> bool:
    import streamlit as st
    if st.session_state.get("X_train") is None:
        st.warning("Data has not been split yet. Please complete **Preprocessing** first.")
        return False
    return True


def validate_pipeline_exists() -> bool:
    if st.session_state.get("pipeline") is None:
        st.warning("No trained model found. Please complete **Train Model** first.")
        return False
    return True
