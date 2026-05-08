import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from utils.config import RANDOM_STATE, DEFAULT_TEST_SIZE
from utils.preprocessing import encode_target
from utils.model_factory import build_pipeline, get_classifier, get_regressor


def split_data(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str,
    task_type: str,
    test_size: float = DEFAULT_TEST_SIZE,
):
    X = df[feature_cols].copy()
    y = df[target_col].copy()

    y, label_encoder = encode_target(y, task_type)

    stratify = None
    if task_type == "Classification":
        # Only stratify if each class has >= 2 samples
        min_class_count = y.value_counts().min()
        if min_class_count >= 2:
            stratify = y

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=stratify,
    )
    return X_train, X_test, y_train, y_test, label_encoder


def train_pipeline(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor,
    model_name: str,
    task_type: str,
    model_params: dict = None,
):
    model_params = model_params or {}
    if task_type == "Classification":
        model = get_classifier(model_name, model_params)
    else:
        model = get_regressor(model_name, model_params)

    pipeline = build_pipeline(preprocessor, model)
    pipeline.fit(X_train, y_train)
    return pipeline


def run_cross_validation(pipeline, X_train, y_train, task_type: str, cv: int = 5):
    scoring = "accuracy" if task_type == "Classification" else "r2"
    scores = cross_val_score(
        pipeline, X_train, y_train,
        cv=cv, scoring=scoring, n_jobs=-1,
    )
    return scores
