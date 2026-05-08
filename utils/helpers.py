import io
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def read_csv_cached(data: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(data))


@st.cache_data(show_spinner=False)
def read_excel_cached(data: bytes) -> pd.DataFrame:
    return pd.read_excel(io.BytesIO(data))


def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    raw = uploaded_file.read()
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if ext == "csv":
        return read_csv_cached(raw)
    else:
        return read_excel_cached(raw)


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def metric_cards(metrics: dict, cols_per_row: int = 5):
    items = list(metrics.items())
    for i in range(0, len(items), cols_per_row):
        batch = items[i:i + cols_per_row]
        cols = st.columns(len(batch))
        for col, (name, val) in zip(cols, batch):
            if isinstance(val, float):
                col.metric(name, f"{val:.4f}")
            else:
                col.metric(name, str(val))


def sidebar_status():
    df = st.session_state.get("df")
    target = st.session_state.get("target_col")
    task = st.session_state.get("task_type")
    pipeline = st.session_state.get("pipeline")
    model_name = st.session_state.get("trained_model_name")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**📌 Session Status**")
    if df is not None:
        st.sidebar.write(f"📁 Dataset: `{st.session_state.get('filename', 'loaded')}`")
        st.sidebar.write(f"   {df.shape[0]} rows × {df.shape[1]} cols")
    else:
        st.sidebar.write("📁 No dataset loaded")

    if target:
        st.sidebar.write(f"🎯 Target: `{target}` ({task})")

    x_train = st.session_state.get("X_train")
    if x_train is not None:
        x_test = st.session_state.get("X_test")
        st.sidebar.write(f"✂️ Split: {x_train.shape[0]} train / {x_test.shape[0]} test")

    if pipeline and model_name:
        st.sidebar.write(f"🤖 Model: `{model_name}`")
        mr = st.session_state.get("model_results", {})
        if mr:
            m = mr.get("metrics", {})
            primary = list(m.items())[0] if m else None
            if primary:
                st.sidebar.write(f"   {primary[0]}: {primary[1]:.4f}")
