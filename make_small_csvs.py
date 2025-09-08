import pandas as pd
from pathlib import Path

big_csv = Path.home() / "Desktop/CS202-Lab4/outputs/diff_comparison_allrepos.csv"
sample_full_csv = Path.home() / "Desktop/CS202-Lab4/outputs/diff_sample_20.csv"
sample_mix_csv = Path.home() / "Desktop/CS202-Lab4/outputs/diff_yes_no_sample_20.csv"


print("Creating small CSV with first 20 rows of the full dataset...")
df_sample = pd.read_csv(big_csv, nrows=20)
df_sample.to_csv(sample_full_csv, index=False)

print("Creating small CSV with 10 'Yes' and 10 'No' rows...")

yes_rows = []
no_rows = []

chunksize = 50000  
for chunk in pd.read_csv(big_csv, chunksize=chunksize):
    yes_chunk = chunk[chunk["Discrepancy"] == "Yes"]
    no_chunk = chunk[chunk["Discrepancy"] == "No"]

    if len(yes_rows) < 10:
        yes_rows.append(yes_chunk.head(10 - len(yes_rows)))
    if len(no_rows) < 10:
        no_rows.append(no_chunk.head(10 - len(no_rows)))

    if sum(len(x) for x in yes_rows) >= 10 and sum(len(x) for x in no_rows) >= 10:
        break

df_yes = pd.concat(yes_rows)
df_no = pd.concat(no_rows)
df_mix = pd.concat([df_yes, df_no]).sample(frac=1, random_state=42)  # shuffle

df_mix.to_csv(sample_mix_csv, index=False)

print(f"Saved sample full CSV: {sample_full_csv}")
print(f"Saved sample mixed CSV: {sample_mix_csv}")
