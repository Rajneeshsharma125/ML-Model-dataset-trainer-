APP_TITLE = "HyperTuneML Platform"
APP_ICON = "🤖"

RANDOM_STATE = 42
DEFAULT_TEST_SIZE = 0.2

CLASSIFICATION_MODELS = [
    "Logistic Regression",
    "Decision Tree",
    "Random Forest",
    "K-Nearest Neighbors",
    "Support Vector Machine",
]

REGRESSION_MODELS = [
    "Linear Regression",
    "Random Forest Regressor",
]

ALL_MODELS = CLASSIFICATION_MODELS + REGRESSION_MODELS

NUMERIC_IMPUTE_STRATEGIES = ["mean", "median", "most_frequent", "constant"]
CAT_IMPUTE_STRATEGIES = ["most_frequent", "constant"]
SCALER_OPTIONS = ["None", "StandardScaler", "MinMaxScaler", "RobustScaler"]
ENCODER_OPTIONS = ["OneHotEncoder", "OrdinalEncoder"]

SIDEBAR_INFO_KEY = "sidebar_info_shown"
