"""
Read raw CSV, clean, engineer features, write processed CSV and insert into SQLite.
"""
import pandas as pd
from pathlib import Path
import sqlite3

RAW = Path("data/raw/student_records.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED = PROCESSED_DIR / "processed.csv"
DB_PATH = "student_records.db"

def load_and_clean():
    df = pd.read_csv(RAW)
    # Basic cleaning
    df = df.drop_duplicates(subset=["student_id"])
    df["attendance"] = df["attendance"].clip(0, 100)
    df["hw_avg"] = df["hw_avg"].clip(0, 100)
    df["midterm"] = df["midterm"].clip(0, 100)
    # Feature engineering examples
    df["attendance_rate"] = df["attendance"] / 100.0
    df["homework_ratio"] = df["hw_avg"] / 100.0
    df["score_gap"] = df["midterm"] - df["prev_gpa"] * 10.0
    # Keep relevant features and label
    features = ["student_id", "attendance_rate", "homework_ratio", "midterm", "prev_gpa", "extracurricular", "at_risk"]
    df = df[features]
    df.to_csv(PROCESSED, index=False)
    print(f"Processed data saved to {PROCESSED}")
    return df

def save_to_sql(df):
    conn = sqlite3.connect(DB_PATH)
    # Create tables using schema file if not exists
    with open("sql/schema.sql", "r") as f:
        conn.executescript(f.read())
    # Insert students and records
    students = df[["student_id"]].drop_duplicates()
    students["name"] = students["student_id"].apply(lambda x: f"Student_{x}")
    students.to_sql("students", conn, if_exists="append", index=False)
    # Prepare records (prediction field left null for now)
    records = df.copy()
    records = records.rename(columns={"at_risk": "at_risk"})
    records["prediction"] = None
    records.to_sql("records", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print("Saved processed data to SQLite DB (student_records.db)")

if __name__ == "__main__":
    df = load_and_clean()
    save_to_sql(df)
