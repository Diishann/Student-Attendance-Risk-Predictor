"""
Train a Logistic Regression model on preprocessed data and save the model + scaler.
"""
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

PROCESSED = Path("data/processed/processed.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_and_save():
    df = pd.read_csv(PROCESSED)
    # Features & label
    X = df[["attendance_rate", "homework_ratio", "midterm", "prev_gpa", "extracurricular"]]
    y = df["at_risk"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(solver="liblinear", class_weight="balanced", random_state=42))
    ])

    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="f1")
    print("CV F1 scores:", cv_scores)
    print("Mean CV F1:", cv_scores.mean())

    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, MODEL_DIR / "logistic_model.joblib")
    print("Model saved to models/logistic_model.joblib")

if __name__ == "__main__":
    train_and_save()
