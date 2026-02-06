"""
Simple synthetic dataset generator for prototyping.
Creates data/raw/student_records.csv
"""
import csv
import random
from pathlib import Path

OUT = Path("data/raw")
OUT.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT / "student_records.csv"

random.seed(42)

def generate(n=500):
    header = ["student_id", "attendance", "hw_avg", "midterm", "prev_gpa", "extracurricular", "at_risk"]
    rows = []
    for i in range(1, n + 1):
        attendance = round(random.normalvariate(80, 10), 1)  # percent
        hw_avg = round(random.normalvariate(75, 12), 1)
        midterm = round(random.normalvariate(70, 15), 1)
        prev_gpa = round(max(0, min(10, random.normalvariate(7, 1.2))), 2)
        extracurricular = round(max(0, random.normalvariate(3, 2)), 1)
        # Heuristic label: low attendance / low hw / low prev_gpa => at risk
        risk_score = (60 - attendance) * 0.02 + (50 - hw_avg) * 0.015 + (6 - prev_gpa) * 0.1
        at_risk = 1 if risk_score > 0.15 or midterm < 40 else 0
        rows.append([i, attendance, hw_avg, midterm, prev_gpa, extracurricular, at_risk])
    with open(OUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Generated {n} rows -> {OUT_FILE}")

if __name__ == "__main__":
    generate(600)
