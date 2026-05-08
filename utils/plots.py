import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


# ── Confusion Matrix ────────────────────────────────────────────────────────
def fig_confusion_matrix(cm, class_names=None):
    labels = class_names if class_names is not None else np.arange(cm.shape[0])
    fig, ax = plt.subplots(figsize=(max(5, cm.shape[0]), max(4, cm.shape[0] - 1)))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    return fig


# ── ROC Curve ───────────────────────────────────────────────────────────────
def fig_roc_curve(fpr, tpr, auc_score: float):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, color="darkorange", lw=2,
            label=f"ROC Curve (AUC = {auc_score:.4f})")
    ax.plot([0, 1], [0, 1], color="navy", lw=1.5, linestyle="--")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver Operating Characteristic")
    ax.legend(loc="lower right")
    plt.tight_layout()
    return fig


# ── Feature Importance ──────────────────────────────────────────────────────
def fig_feature_importance(pipeline, top_n: int = 20):
    model = pipeline.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        coef = model.coef_
        importances = np.abs(coef).mean(axis=0) if coef.ndim > 1 else np.abs(coef)
    else:
        return None

    try:
        feat_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    except Exception:
        feat_names = [f"Feature_{i}" for i in range(len(importances))]

    if len(importances) != len(feat_names):
        feat_names = [f"Feature_{i}" for i in range(len(importances))]

    df_imp = pd.DataFrame({"Feature": feat_names, "Importance": importances})
    df_imp = df_imp.sort_values("Importance", ascending=True).tail(top_n)

    fig = px.bar(
        df_imp, x="Importance", y="Feature", orientation="h",
        title=f"Feature Importance (Top {top_n})",
        color="Importance", color_continuous_scale="Blues",
    )
    fig.update_layout(height=max(350, top_n * 22), yaxis_title="")
    return fig


# ── Actual vs Predicted ─────────────────────────────────────────────────────
def fig_actual_vs_predicted(y_test, y_pred):
    mn = min(float(np.min(y_test)), float(np.min(y_pred)))
    mx = max(float(np.max(y_test)), float(np.max(y_pred)))
    fig = px.scatter(x=list(y_test), y=list(y_pred),
                     labels={"x": "Actual", "y": "Predicted"},
                     title="Actual vs Predicted", opacity=0.7)
    fig.add_shape(type="line", x0=mn, y0=mn, x1=mx, y1=mx,
                  line=dict(color="red", dash="dash", width=2))
    return fig


# ── Residuals ───────────────────────────────────────────────────────────────
def fig_residuals(y_test, y_pred):
    residuals = np.array(y_test) - np.array(y_pred)
    fig = px.scatter(x=list(y_pred), y=list(residuals),
                     labels={"x": "Predicted", "y": "Residual"},
                     title="Residual Plot", opacity=0.7)
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    return fig


# ── Distribution ─────────────────────────────────────────────────────────────
def fig_histogram(df: pd.DataFrame, col: str, target_col: str = None):
    color = None
    if target_col and target_col in df.columns and df[target_col].nunique() <= 12:
        color = target_col
    fig = px.histogram(df, x=col, color=color, marginal="box",
                       title=f"Distribution — {col}", barmode="overlay",
                       opacity=0.75)
    return fig


# ── Box Plot ─────────────────────────────────────────────────────────────────
def fig_box(df: pd.DataFrame, col: str, target_col: str = None):
    color = None
    y_col = col
    x_col = None
    if target_col and target_col in df.columns and df[target_col].nunique() <= 12:
        x_col = target_col
    fig = px.box(df, x=x_col, y=y_col, color=x_col,
                 title=f"Box Plot — {col}")
    return fig


# ── Scatter Plot ─────────────────────────────────────────────────────────────
def fig_scatter(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = None):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                     trendline="ols" if color_col is None else None,
                     title=f"{x_col} vs {y_col}", opacity=0.75)
    return fig


# ── Correlation Heatmap ──────────────────────────────────────────────────────
def fig_correlation_heatmap(df: pd.DataFrame):
    num_df = df.select_dtypes(include=[np.number])
    if num_df.shape[1] < 2:
        return None
    corr = num_df.corr()
    size = max(6, len(corr) * 0.65)
    fig, ax = plt.subplots(figsize=(size, size * 0.85))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                ax=ax, linewidths=0.4, square=True)
    ax.set_title("Correlation Heatmap")
    plt.tight_layout()
    return fig


# ── Model Comparison Bar ─────────────────────────────────────────────────────
def fig_model_comparison(compare_df: pd.DataFrame, metric: str):
    df_sorted = compare_df.dropna(subset=[metric]).sort_values(metric, ascending=True)
    fig = px.bar(df_sorted, x=metric, y="Model", orientation="h",
                 color=metric, color_continuous_scale="Blues",
                 title=f"Model Comparison — {metric}")
    fig.update_layout(height=max(300, len(df_sorted) * 55))
    return fig


# ── Radar Chart ──────────────────────────────────────────────────────────────
def fig_radar(compare_df: pd.DataFrame, metrics: list):
    fig = go.Figure()
    for _, row in compare_df.iterrows():
        vals = [float(row.get(m, 0) or 0) for m in metrics]
        vals.append(vals[0])
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=metrics + [metrics[0]],
            fill="toself",
            name=str(row["Model"]),
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Model Comparison Radar",
        showlegend=True,
    )
    return fig
