import pandas as pd

# Load dataset
df = pd.read_csv("evaluation_sample.csv")

# ---- Baseline Statistics ----
print("\n===== Baseline Stats =====")
print("Total commits:", df["Hash"].nunique())
print("Total files:", len(df))
print("Average modified files per commit:", df.groupby("Hash")["Filename"].count().mean())

print("\nDistribution of fix types (LLM Inference):")
print(df["LLM Inference (fix type)"].value_counts())

print("\nMost frequently modified file extensions:")
print(df["Filename"].str.split(".").str[-1].value_counts().head())

# ---- Save CSV snapshot ----
df.to_csv("part_b_baseline.csv", index=False)
print("\nPart B complete: results saved in part_b_baseline.csv")
