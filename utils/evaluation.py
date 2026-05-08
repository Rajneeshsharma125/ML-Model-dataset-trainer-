import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score, roc_curve, classification_report,
    mean_squared_error, mean_absolute_error, r2_score,
)


def evaluate_classifier(pipeline, X_test, y_test, label_encoder=None):
    y_pred = pipeline.predict(X_test)
    n_classes = int(len(np.unique(y_test)))
    avg = "binary" if n_classes == 2 else "weighted"

    metrics = {
        "Accuracy":  round(float(accuracy_score(y_test, y_pred)), 4),
        "Precision": round(float(precision_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "Recall":    round(float(recall_score(y_test, y_pred, average=avg, zero_division=0)), 4),
        "F1 Score":  round(float(f1_score(y_test, y_pred, average=avg, zero_division=0)), 4),
    }

    # ROC-AUC
    fpr_tpr = None
    roc_auc = None
    try:
        y_proba = pipeline.predict_proba(X_test)
        if n_classes == 2:
            roc_auc = round(float(roc_auc_score(y_test, y_proba[:, 1])), 4)
            fpr, tpr, _ = roc_curve(y_test, y_proba[:, 1])
            fpr_tpr = (fpr, tpr)
        else:
            roc_auc = round(float(roc_auc_score(y_test, y_proba, multi_class="ovr")), 4)
        metrics["ROC-AUC"] = roc_auc
    except Exception:
        pass

    cm = confusion_matrix(y_test, y_pred)
    class_names = list(label_encoder.classes_) if label_encoder is not None else None
    target_names = [str(c) for c in class_names] if class_names else None
    report = classification_report(y_test, y_pred, target_names=target_names, zero_division=0)

    return metrics, cm, fpr_tpr, class_names, report


def evaluate_regressor(pipeline, X_test, y_test):
    y_pred = pipeline.predict(X_test)
    mse = float(mean_squared_error(y_test, y_pred))
    metrics = {
        "R² Score": round(float(r2_score(y_test, y_pred)), 4),
        "MAE":      round(float(mean_absolute_error(y_test, y_pred)), 4),
        "MSE":      round(mse, 4),
        "RMSE":     round(float(np.sqrt(mse)), 4),
    }
    return metrics, np.array(y_pred)


def bulk_compare_classifiers(pipelines: dict, X_train, X_test, y_train, y_test) -> pd.DataFrame:
    rows = []
    n_classes = int(len(np.unique(y_test)))
    avg = "binary" if n_classes == 2 else "weighted"
    for name, pipe in pipelines.items():
        row = {"Model": name}
        try:
            pipe.fit(X_train, y_train)
            y_pred = pipe.predict(X_test)
            row["Accuracy"]  = round(float(accuracy_score(y_test, y_pred)), 4)
            row["Precision"] = round(float(precision_score(y_test, y_pred, average=avg, zero_division=0)), 4)
            row["Recall"]    = round(float(recall_score(y_test, y_pred, average=avg, zero_division=0)), 4)
            row["F1 Score"]  = round(float(f1_score(y_test, y_pred, average=avg, zero_division=0)), 4)
            try:
                yp = pipe.predict_proba(X_test)
                if n_classes == 2:
                    row["ROC-AUC"] = round(float(roc_auc_score(y_test, yp[:, 1])), 4)
                else:
                    row["ROC-AUC"] = round(float(roc_auc_score(y_test, yp, multi_class="ovr")), 4)
            except Exception:
                row["ROC-AUC"] = None
        except Exception as e:
            row["Error"] = str(e)
        rows.append(row)
    return pd.DataFrame(rows)


def bulk_compare_regressors(pipelines: dict, X_train, X_test, y_train, y_test) -> pd.DataFrame:
    rows = []
    for name, pipe in pipelines.items():
        row = {"Model": name}
        try:
            pipe.fit(X_train, y_train)
            y_pred = pipe.predict(X_test)
            mse = float(mean_squared_error(y_test, y_pred))
            row["R² Score"] = round(float(r2_score(y_test, y_pred)), 4)
            row["MAE"]      = round(float(mean_absolute_error(y_test, y_pred)), 4)
            row["RMSE"]     = round(float(np.sqrt(mse)), 4)
        except Exception as e:
            row["Error"] = str(e)
        rows.append(row)
    return pd.DataFrame(rows)
