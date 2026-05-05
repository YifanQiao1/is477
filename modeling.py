import os
from pathlib import Path

import numpy as np
import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", ".mplconfig")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
FIGURES_DIR = Path("figures")
FIGURES_DIR.mkdir(exist_ok=True)


df = pd.read_csv("merged_data.csv")

# Use the existing merged target so this script matches the cleaning, EDA, and
# project documentation. Do not train on injury fields used to create it.
target_col = "severe_crash"
group_col = "crash_record_id"

leakage_cols = [
    "most_severe_injury",
    "injuries_total",
    "injuries_fatal",
    "injury_level",
]

identifier_or_high_cardinality_cols = [
    "crash_record_id",
    "crash_unit_id",
    "vehicle_id",
    "crash_date_x",
    "crash_date_y",
    "crash_date_vehicle",
    "crash_date_crash",
]

drop_cols = [
    target_col,
    *leakage_cols,
    *identifier_or_high_cardinality_cols,
]

df_model = df.dropna(subset=[target_col, group_col]).copy()
groups = df_model[group_col]
y = df_model[target_col].astype(int)
X = df_model.drop(columns=[col for col in drop_cols if col in df_model.columns])


def save_class_balance_plot(y_values):
    plt.figure(figsize=(6, 4))
    ax = sns.countplot(x=y_values)
    ax.set_title("Crash Severity Class Balance")
    ax.set_xlabel("Severe crash")
    ax.set_ylabel("Rows")
    ax.bar_label(ax.containers[0])
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "model_class_balance.png", dpi=300)
    plt.close()


save_class_balance_plot(y)

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=RANDOM_STATE,
)
train_idx, test_idx = next(splitter.split(X, y, groups=groups))

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]
y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

cat_cols = X.select_dtypes(include=["object", "category"]).columns
num_cols = X.select_dtypes(exclude=["object", "category"]).columns

numeric_transformer = Pipeline(
    [
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)

categorical_transformer = Pipeline(
    [
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocessor = ColumnTransformer(
    [
        ("num", numeric_transformer, num_cols),
        ("cat", categorical_transformer, cat_cols),
    ]
)

models = {
    "Logistic Regression": Pipeline(
        [
            ("prep", preprocessor),
            (
                "clf",
                LogisticRegression(
                    max_iter=3000,
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    ),
    "Random Forest": Pipeline(
        [
            ("prep", preprocessor),
            (
                "clf",
                RandomForestClassifier(
    n_estimators=50,
    max_depth=12,
    min_samples_leaf=20,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    class_weight="balanced",
),
            ),
        ]
    ),
}

model_results = {}

for model_name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    roc_auc = roc_auc_score(y_test, proba)
    avg_precision = average_precision_score(y_test, proba)
    model_results[model_name] = {
        "model": model,
        "pred": pred,
        "proba": proba,
        "roc_auc": roc_auc,
        "average_precision": avg_precision,
    }

    print(f"=== {model_name} ===")
    print(classification_report(y_test, pred))
    print("ROC-AUC:", roc_auc)
    print("Average precision:", avg_precision)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, pred))


def safe_file_label(model_name):
    return model_name.lower().replace(" ", "_")


def save_confusion_matrix_plot(model_name, y_true, y_pred):
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=["Not severe", "Severe"],
        cmap="Blues",
        values_format="d",
        ax=ax,
    )
    ax.set_title(f"{model_name} Confusion Matrix")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{safe_file_label(model_name)}_confusion_matrix.png", dpi=300)
    plt.close(fig)


def save_roc_curve_plot(results):
    fig, ax = plt.subplots(figsize=(6, 5))
    for model_name, result in results.items():
        RocCurveDisplay.from_predictions(
            y_test,
            result["proba"],
            name=f"{model_name} (AUC={result['roc_auc']:.3f})",
            ax=ax,
        )
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random")
    ax.set_title("ROC Curves")
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "model_roc_curves.png", dpi=300)
    plt.close(fig)


def save_precision_recall_curve_plot(results):
    fig, ax = plt.subplots(figsize=(6, 5))
    baseline = y_test.mean()
    for model_name, result in results.items():
        PrecisionRecallDisplay.from_predictions(
            y_test,
            result["proba"],
            name=f"{model_name} (AP={result['average_precision']:.3f})",
            ax=ax,
        )
    ax.axhline(
        baseline,
        linestyle="--",
        color="gray",
        label=f"Baseline positive rate ({baseline:.3f})",
    )
    ax.set_title("Precision-Recall Curves")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "model_precision_recall_curves.png", dpi=300)
    plt.close(fig)


def save_threshold_curve_plot(model_name, y_true, proba):
    precision, recall, thresholds = precision_recall_curve(y_true, proba)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(thresholds, precision[:-1], label="Precision")
    ax.plot(thresholds, recall[:-1], label="Recall")
    ax.set_title(f"{model_name} Precision/Recall by Threshold")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{safe_file_label(model_name)}_threshold_curve.png", dpi=300)
    plt.close(fig)


def get_feature_names(fitted_model):
    preprocessor_step = fitted_model.named_steps["prep"]
    feature_names = []

    if len(num_cols) > 0:
        feature_names.extend(num_cols)

    if len(cat_cols) > 0:
        onehot = preprocessor_step.named_transformers_["cat"].named_steps["onehot"]
        feature_names.extend(onehot.get_feature_names_out(cat_cols))

    return np.array(feature_names)


def save_random_forest_feature_importance_plot(fitted_model):
    feature_names = get_feature_names(fitted_model)
    importances = fitted_model.named_steps["clf"].feature_importances_
    feat_imp = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .sort_values(by="importance", ascending=False)
        .head(20)
    )

    plt.figure(figsize=(8, 7))
    ax = sns.barplot(data=feat_imp, y="feature", x="importance", color="#4C78A8")
    ax.set_title("Random Forest Top Feature Importances")
    ax.set_xlabel("Importance")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "random_forest_feature_importance.png", dpi=300)
    plt.close()

    feat_imp.to_csv(FIGURES_DIR / "random_forest_top_features.csv", index=False)


for model_name, result in model_results.items():
    save_confusion_matrix_plot(model_name, y_test, result["pred"])
    save_threshold_curve_plot(model_name, y_test, result["proba"])

save_roc_curve_plot(model_results)
save_precision_recall_curve_plot(model_results)
save_random_forest_feature_importance_plot(model_results["Random Forest"]["model"])

print(f"\nSaved model visualizations to: {FIGURES_DIR.resolve()}")

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

metrics_rows = []

for model_name, result in model_results.items():
    pred = result["pred"]
    proba = result["proba"]

    metrics_rows.append({
        "model": model_name,
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0),
        "roc_auc": result["roc_auc"],
        "average_precision": result["average_precision"],
        "test_positive_rate": y_test.mean(),
        "n_train": len(y_train),
        "n_test": len(y_test),
    })

metrics_df = pd.DataFrame(metrics_rows)
metrics_df.to_csv(FIGURES_DIR / "model_metrics.csv", index=False)

print("\nSaved model metrics to:", FIGURES_DIR / "model_metrics.csv")
print(metrics_df)