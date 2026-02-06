"""
Use trained model to produce predictions and save predictions.csv and write back to DB.
"""
import pandas as pd
import joblib
import sqlite3
from pathlib import Path

PROCESSED = Path("data/processed/processed.csv")
MODEL = Path("models/logistic_model.joblib")
OUT_FILE = Path("data/predictions.csv")
DB_PATH = "student_records.db"

def predict_and_persist():
    df = pd.read_csv(PROCESSED)
    X = df[["attendance_rate", "homework_ratio", "midterm", "prev_gpa", "extracurricular"]]
    model = joblib.load(MODEL)
    preds = model.predict(X)
    df["prediction"] = preds
    df[["student_id", "prediction"]].to_csv(OUT_FILE, index=False)
    print(f"Predictions written to {OUT_FILE}")

    # Write predictions into the SQLite records table
    conn = sqlite3.connect(DB_PATH)
    for _, row in df.iterrows():
        conn.execute("UPDATE records SET prediction = ? WHERE student_id = ? AND prediction IS NULL", (int(row.prediction), int(row.student_id)))
    conn.commit()
    conn.close()
    print("Predictions updated in SQLite DB.")

if __name__ == "__main__":
    predict_and_persist()
