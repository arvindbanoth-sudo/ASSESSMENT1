import pandas as pd
from pathlib import Path


csv_path = Path.home() / "Desktop/CS202-Lab4/outputs/diff_comparison_allrepos.csv"

print("Loading CSV (only necessary columns)...")
df = pd.read_csv(csv_path, usecols=["file_type", "Discrepancy"])


mismatches = df[df["Discrepancy"] == "Yes"]


summary = mismatches.groupby("file_type").size().reset_index(name="mismatch_count")


summary_path = Path.home() / "Desktop/CS202-Lab4/outputs/mismatch_summary.csv"
summary.to_csv(summary_path, index=False)

print("\nSummary of mismatches by file type:")
print(summary)
print(f"\nSaved small summary CSV to: {summary_path}")
