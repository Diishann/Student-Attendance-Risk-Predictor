"""
Copy predictions CSV into web/ folder for static dashboard consumption.
This lets index.html fetch './data/predictions.csv' when served.
"""
from pathlib import Path
import shutil

SRC = Path("data/predictions.csv")
DEST = Path("web/data")
DEST.mkdir(parents=True, exist_ok=True)
DEST_FILE = DEST / "predictions.csv"

if __name__ == "__main__":
    if SRC.exists():
        shutil.copy(SRC, DEST_FILE)
        print(f"Copied {SRC} -> {DEST_FILE}")
    else:
        print(f"{SRC} not found. Run predict.py first.")
