from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from utils.config import RANDOM_STATE


def get_classifier(name: str, params: dict = None):
    p = params or {}
    rs = RANDOM_STATE
    mapping = {
        "Logistic Regression": LogisticRegression(
            C=p.get("C", 1.0),
            max_iter=p.get("max_iter", 1000),
            random_state=rs,
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=p.get("max_depth", None),
            min_samples_split=p.get("min_samples_split", 2),
            min_samples_leaf=p.get("min_samples_leaf", 1),
            random_state=rs,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=p.get("n_estimators", 100),
            max_depth=p.get("max_depth", None),
            random_state=rs,
        ),
        "K-Nearest Neighbors": KNeighborsClassifier(
            n_neighbors=p.get("n_neighbors", 5),
            weights=p.get("weights", "uniform"),
        ),
        "Support Vector Machine": SVC(
            C=p.get("C", 1.0),
            kernel=p.get("kernel", "rbf"),
            probability=True,
            random_state=rs,
        ),
    }
    if name not in mapping:
        raise ValueError(f"Unknown classifier: {name}")
    return mapping[name]


def get_regressor(name: str, params: dict = None):
    p = params or {}
    rs = RANDOM_STATE
    mapping = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=p.get("n_estimators", 100),
            max_depth=p.get("max_depth", None),
            random_state=rs,
        ),
    }
    if name not in mapping:
        raise ValueError(f"Unknown regressor: {name}")
    return mapping[name]


def build_pipeline(preprocessor, model) -> Pipeline:
    return Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ])


def classifier_param_widgets(name: str, st_obj) -> dict:
    params = {}
    if name == "Logistic Regression":
        params["C"] = st_obj.slider("Regularization C", 0.01, 10.0, 1.0, step=0.01,
                                    key="lr_C")
        params["max_iter"] = st_obj.slider("Max Iterations", 100, 5000, 1000, step=100,
                                           key="lr_maxiter")
    elif name == "Decision Tree":
        raw_depth = st_obj.slider("Max Depth (0 = unlimited)", 0, 30, 0, key="dt_depth")
        params["max_depth"] = None if raw_depth == 0 else raw_depth
        params["min_samples_split"] = st_obj.slider("Min Samples Split", 2, 20, 2, key="dt_mss")
        params["min_samples_leaf"] = st_obj.slider("Min Samples Leaf", 1, 10, 1, key="dt_msl")
    elif name == "Random Forest":
        params["n_estimators"] = st_obj.slider("Number of Trees", 10, 500, 100, step=10,
                                               key="rf_trees")
        raw_depth = st_obj.slider("Max Depth (0 = unlimited)", 0, 30, 0, key="rf_depth")
        params["max_depth"] = None if raw_depth == 0 else raw_depth
    elif name == "K-Nearest Neighbors":
        params["n_neighbors"] = st_obj.slider("Number of Neighbors (k)", 1, 30, 5, key="knn_k")
        params["weights"] = st_obj.selectbox("Weights", ["uniform", "distance"], key="knn_w")
    elif name == "Support Vector Machine":
        params["C"] = st_obj.slider("Regularization C", 0.01, 10.0, 1.0, step=0.01, key="svm_C")
        params["kernel"] = st_obj.selectbox("Kernel", ["rbf", "linear", "poly", "sigmoid"],
                                            key="svm_kernel")
    return params


def regressor_param_widgets(name: str, st_obj) -> dict:
    params = {}
    if name == "Random Forest Regressor":
        params["n_estimators"] = st_obj.slider("Number of Trees", 10, 500, 100, step=10,
                                               key="rfr_trees")
        raw_depth = st_obj.slider("Max Depth (0 = unlimited)", 0, 30, 0, key="rfr_depth")
        params["max_depth"] = None if raw_depth == 0 else raw_depth
    return params
