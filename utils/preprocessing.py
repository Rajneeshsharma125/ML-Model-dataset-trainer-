import pandas as pd
import numpy as np
import streamlit as st
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    OneHotEncoder, OrdinalEncoder, LabelEncoder,
)


def detect_column_types(df: pd.DataFrame, feature_cols: list):
    numeric_cols, categorical_cols = [], []
    for col in feature_cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
        else:
            categorical_cols.append(col)
    return numeric_cols, categorical_cols


def auto_detect_task(df: pd.DataFrame, target_col: str) -> str:
    if not pd.api.types.is_numeric_dtype(df[target_col]):
        return "Classification"
    n_unique = df[target_col].nunique()
    return "Classification" if n_unique <= 15 else "Regression"


@st.cache_data
def get_missing_report(df: pd.DataFrame) -> pd.DataFrame:
    miss = df.isnull().sum()
    pct = (miss / len(df) * 100).round(2)
    return pd.DataFrame({
        "Missing Count": miss,
        "Missing %": pct,
        "Dtype": df.dtypes,
    }).sort_values("Missing Count", ascending=False)


def build_preprocessor(
    numeric_cols: list,
    categorical_cols: list,
    numeric_impute: str = "mean",
    scaler: str = "StandardScaler",
    cat_impute: str = "most_frequent",
    encoder: str = "OneHotEncoder",
) -> ColumnTransformer:
    # Numeric pipeline
    num_steps = [("imputer", SimpleImputer(strategy=numeric_impute))]
    if scaler == "StandardScaler":
        num_steps.append(("scaler", StandardScaler()))
    elif scaler == "MinMaxScaler":
        num_steps.append(("scaler", MinMaxScaler()))
    elif scaler == "RobustScaler":
        num_steps.append(("scaler", RobustScaler()))
    num_pipe = Pipeline(steps=num_steps)

    # Categorical pipeline
    if encoder == "OneHotEncoder":
        enc_obj = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    else:
        enc_obj = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)

    cat_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy=cat_impute, fill_value="missing")),
        ("encoder", enc_obj),
    ])

    transformers = []
    if numeric_cols:
        transformers.append(("num", num_pipe, numeric_cols))
    if categorical_cols:
        transformers.append(("cat", cat_pipe, categorical_cols))

    if not transformers:
        return ColumnTransformer(transformers=[], remainder="passthrough")

    return ColumnTransformer(transformers=transformers, remainder="drop")


def encode_target(y: pd.Series, task_type: str):
    if task_type == "Classification" and not pd.api.types.is_numeric_dtype(y):
        le = LabelEncoder()
        return pd.Series(le.fit_transform(y), index=y.index, name=y.name), le
    return y, None
