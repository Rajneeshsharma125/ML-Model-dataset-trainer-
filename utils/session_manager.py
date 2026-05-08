import streamlit as st


_DEFAULTS = {
    # Data
    "df_raw": None,
    "df": None,
    "filename": "",
    # Config
    "target_col": None,
    "feature_cols": [],
    "task_type": None,
    # Splits
    "X_train": None,
    "X_test": None,
    "y_train": None,
    "y_test": None,
    "label_encoder": None,
    # Preprocessing
    "preprocessing_config": {},
    "preprocessor": None,
    # Training
    "pipeline": None,
    "trained_model_name": None,
    "model_results": {},
    "cv_scores": None,
    # Compare
    "compare_df": None,
}


def init_session_state():
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_downstream(from_step: str):
    """Clear all state downstream of a given step."""
    steps = ["data", "preprocessing", "training", "compare"]
    idx = steps.index(from_step) if from_step in steps else 0
    if idx <= 0:
        for k in ["df_raw", "df", "filename", "target_col", "feature_cols",
                  "task_type", "X_train", "X_test", "y_train", "y_test",
                  "label_encoder", "preprocessing_config", "preprocessor",
                  "pipeline", "trained_model_name", "model_results",
                  "cv_scores", "compare_df"]:
            st.session_state[k] = _DEFAULTS[k]
    elif idx <= 1:
        for k in ["X_train", "X_test", "y_train", "y_test", "label_encoder",
                  "preprocessing_config", "preprocessor",
                  "pipeline", "trained_model_name", "model_results",
                  "cv_scores", "compare_df"]:
            st.session_state[k] = _DEFAULTS[k]
    elif idx <= 2:
        for k in ["pipeline", "trained_model_name", "model_results",
                  "cv_scores", "compare_df"]:
            st.session_state[k] = _DEFAULTS[k]
    elif idx <= 3:
        st.session_state["compare_df"] = None


def get(key, default=None):
    return st.session_state.get(key, default)


def set_val(key, value):
    st.session_state[key] = value
