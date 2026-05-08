# HyperTuneML Platform

A complete end-to-end Machine Learning web application built with Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ml-data-trainer-database-using-app-bifajunxnbstryzcha7mfb.streamlit.app/)

## Features

- CSV / XLSX upload with preview and validation
- Missing values report and duplicate removal
- Preprocessing via sklearn Pipeline + ColumnTransformer (zero data leakage)
- Full EDA dashboard: histograms, heatmaps, scatter plots, box plots
- Classification & Regression support
- Model comparison across multiple algorithms
- Confusion matrix, ROC curve, feature importance
- Single and batch prediction using saved pipeline
- Downloadable model (.joblib) and metadata (.json)
- Pipeline persistence with joblib
- Streamlit Cloud compatible

## Models Supported

**Classification:** Logistic Regression, Decision Tree, Random Forest, KNN, SVM

**Regression:** Linear Regression, Random Forest Regressor

## Project Structure

```
app.py
requirements.txt
README.md
utils/
    __init__.py
    config.py
    validators.py
    session_manager.py
    preprocessing.py
    model_factory.py
    training.py
    evaluation.py
    persistence.py
    plots.py
    helpers.py
pages/
    01_Upload_Data.py
    02_Preprocessing.py
    03_EDA.py
    04_Train_Model.py
    05_Evaluate.py
    06_Compare_Models.py
    07_Predict.py
    08_Download_Model.py
```

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying on Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select the repository and set main file to `app.py`
4. Click Deploy

## Key Implementation Details

- `random_state=42` used throughout for reproducibility
- `stratify=y` applied for classification train/test splits
- Train/test split occurs **before** fitting any preprocessor (no data leakage)
- The full Pipeline (preprocessor + model) is saved so predictions always use identical transformations
- `st.cache_data` and `st.cache_resource` used for performance
- All session state managed centrally via `utils/session_manager.py`

## Libraries

- **Streamlit** — UI framework
- **scikit-learn** — ML algorithms, Pipeline, ColumnTransformer
- **pandas / numpy** — Data manipulation
- **matplotlib / seaborn / plotly** — Visualization
- **joblib** — Model serialization
