"""
Evaluate saved model on test split and output metrics + plots to outputs/.
"""
import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np

PROCESSED = Path("data/processed/processed.csv")
MODEL = Path("models/logistic_model.joblib")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def evaluate():
    df = pd.read_csv(PROCESSED)
    X = df[["attendance_rate", "homework_ratio", "midterm", "prev_gpa", "extracurricular"]]
    y = df["at_risk"]
    # simple holdout: last 20% (same as training script)
    split_idx = int(len(df) * 0.8)
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]

    model = joblib.load(MODEL)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Metrics
    report = classification_report(y_test, y_pred)
    print(report)
    with open(OUT_DIR / "metrics.txt", "w") as f:
        f.write(report)

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5,4))
    plt.imshow(cm, cmap="Blues")
    plt.title("Confusion Matrix")
    plt.colorbar()
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks([0,1])
    plt.yticks([0,1])
    for (i, j), val in np.ndenumerate(cm):
        plt.text(j, i, val, ha='center', va='center')
    plt.savefig(OUT_DIR / "conf_mat.png")
    plt.close()

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    plt.plot([0,1],[0,1],"--", alpha=0.5)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.title("ROC Curve")
    plt.savefig(OUT_DIR / "roc_curve.png")
    plt.close()

    print(f"Saved metrics + plots to {OUT_DIR}")

if __name__ == "__main__":
    evaluate()
