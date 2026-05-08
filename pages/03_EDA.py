import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.session_manager import init_session_state
from utils.helpers import sidebar_status
from utils.validators import validate_dataframe
from utils.preprocessing import get_missing_report
from utils.plots import (
    fig_histogram, fig_box, fig_scatter,
    fig_correlation_heatmap,
)

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
init_session_state()
sidebar_status()

st.title("📊 Exploratory Data Analysis")

df = st.session_state.get("df")
target_col = st.session_state.get("target_col")
feature_cols = st.session_state.get("feature_cols", [])
task_type = st.session_state.get("task_type")

if not validate_dataframe(df):
    st.info("👈 Please complete **Upload Data** first.")
    st.stop()

all_cols = feature_cols + ([target_col] if target_col and target_col not in feature_cols else [])
numeric_feat = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c])]
categorical_feat = [c for c in feature_cols if not pd.api.types.is_numeric_dtype(df[c])]

tab_ov, tab_dist, tab_box, tab_scatter, tab_corr, tab_target = st.tabs([
    "📋 Overview", "📈 Distributions", "📦 Box Plots",
    "🔵 Scatter", "🔥 Correlations", "🎯 Target",
])

# ── Overview ──────────────────────────────────────────────────────────────────
with tab_ov:
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Rows", df.shape[0])
    m2.metric("Columns", df.shape[1])
    m3.metric("Numeric", len(numeric_feat))
    m4.metric("Categorical", len(categorical_feat))
    total_missing = int(df[feature_cols].isnull().sum().sum())
    m5.metric("Missing Cells", total_missing)

    st.markdown("#### Column Info")
    info_rows = []
    for c in all_cols:
        info_rows.append({
            "Column": c,
            "Dtype": str(df[c].dtype),
            "Unique": int(df[c].nunique()),
            "Missing": int(df[c].isnull().sum()),
            "Missing %": round(df[c].isnull().mean() * 100, 2),
            "Sample": str(df[c].dropna().iloc[:3].tolist()) if len(df[c].dropna()) > 0 else "",
        })
    st.dataframe(pd.DataFrame(info_rows), use_container_width=True)

    st.markdown("#### Descriptive Statistics")
    st.dataframe(df[all_cols].describe(include="all").T, use_container_width=True)

# ── Distributions ─────────────────────────────────────────────────────────────
with tab_dist:
    if not all_cols:
        st.info("No columns available.")
    else:
        col_sel = st.selectbox("Select Column", all_cols, key="dist_col")
        st.plotly_chart(fig_histogram(df, col_sel, target_col), use_container_width=True)

        if len(numeric_feat) > 1:
            st.markdown("#### All Numeric Features (Histograms)")
            n_per_row = 3
            groups = [numeric_feat[i:i+n_per_row] for i in range(0, len(numeric_feat), n_per_row)]
            for grp in groups:
                cols_ui = st.columns(len(grp))
                for col_ui, c in zip(cols_ui, grp):
                    with col_ui:
                        fig_sm = px.histogram(df, x=c, title=c, height=240)
                        fig_sm.update_layout(margin=dict(t=30, b=0, l=0, r=0), showlegend=False)
                        st.plotly_chart(fig_sm, use_container_width=True)

# ── Box Plots ─────────────────────────────────────────────────────────────────
with tab_box:
    if not numeric_feat:
        st.info("No numeric feature columns detected.")
    else:
        box_col = st.selectbox("Select Numeric Column", numeric_feat, key="box_col")
        st.plotly_chart(fig_box(df, box_col, target_col), use_container_width=True)

        st.markdown("#### All Numeric Features — Grouped Box Plots")
        import plotly.graph_objects as go
        fig_all_box = go.Figure()
        for c in numeric_feat:
            fig_all_box.add_trace(go.Box(y=df[c].dropna(), name=c))
        fig_all_box.update_layout(title="All Features Box Plot", height=450)
        st.plotly_chart(fig_all_box, use_container_width=True)

# ── Scatter ───────────────────────────────────────────────────────────────────
with tab_scatter:
    if len(numeric_feat) < 2:
        st.info("Need at least 2 numeric feature columns for scatter plots.")
    else:
        sc1, sc2, sc3 = st.columns(3)
        x_col = sc1.selectbox("X Axis", numeric_feat, index=0, key="sc_x")
        y_col = sc2.selectbox("Y Axis", numeric_feat, index=min(1, len(numeric_feat)-1), key="sc_y")
        color_opts = ["None"] + [c for c in all_cols if df[c].nunique() <= 20]
        color_col = sc3.selectbox("Color By", color_opts, key="sc_color")
        color_arg = None if color_col == "None" else color_col
        st.plotly_chart(fig_scatter(df, x_col, y_col, color_arg), use_container_width=True)

# ── Correlations ──────────────────────────────────────────────────────────────
with tab_corr:
    num_df = df[numeric_feat].copy() if numeric_feat else pd.DataFrame()
    if target_col and pd.api.types.is_numeric_dtype(df[target_col]) and target_col not in num_df.columns:
        num_df[target_col] = df[target_col]

    if num_df.shape[1] < 2:
        st.info("Need at least 2 numeric columns for correlation analysis.")
    else:
        heatmap_fig = fig_correlation_heatmap(num_df)
        if heatmap_fig:
            st.pyplot(heatmap_fig)

        if target_col and pd.api.types.is_numeric_dtype(df[target_col]):
            st.markdown(f"#### Feature Correlation with Target: `{target_col}`")
            target_corr = num_df.drop(columns=[target_col], errors="ignore").corrwith(
                df[target_col]
            ).sort_values(key=abs, ascending=False)
            fig_tc = px.bar(
                x=target_corr.index, y=target_corr.values,
                labels={"x": "Feature", "y": "Correlation"},
                color=target_corr.values, color_continuous_scale="RdBu",
                title=f"Correlation with {target_col}",
            )
            st.plotly_chart(fig_tc, use_container_width=True)

# ── Target Analysis ───────────────────────────────────────────────────────────
with tab_target:
    if not target_col:
        st.info("No target column configured.")
    else:
        st.markdown(f"### Target: `{target_col}` — Task: **{task_type}**")
        st.plotly_chart(fig_histogram(df, target_col), use_container_width=True)

        if task_type == "Classification":
            vc = df[target_col].value_counts().reset_index()
            vc.columns = ["Class", "Count"]
            vc["Percentage"] = (vc["Count"] / len(df) * 100).round(2)
            st.dataframe(vc, use_container_width=True)
            max_cls = int(vc["Count"].max())
            min_cls = int(vc["Count"].min())
            ratio = max_cls / min_cls if min_cls > 0 else float("inf")
            if ratio > 4:
                st.warning(f"⚠️ Class imbalance ratio: {ratio:.1f}x — consider resampling techniques.")
            else:
                st.success(f"✅ Class balance ratio: {ratio:.1f}x — balanced enough.")

            fig_pie = px.pie(vc, values="Count", names="Class",
                             title=f"Class Distribution — {target_col}")
            st.plotly_chart(fig_pie, use_container_width=True)

        else:
            stats = df[target_col].describe()
            st.dataframe(stats.to_frame(), use_container_width=True)
            skew = float(df[target_col].skew())
            kurt = float(df[target_col].kurt())
            sk1, sk2 = st.columns(2)
            sk1.metric("Skewness", f"{skew:.4f}")
            sk2.metric("Kurtosis", f"{kurt:.4f}")

            if numeric_feat:
                scatter_x = st.selectbox("Feature vs Target Scatter", numeric_feat, key="tgt_sc")
                st.plotly_chart(
                    fig_scatter(df, scatter_x, target_col),
                    use_container_width=True,
                )
