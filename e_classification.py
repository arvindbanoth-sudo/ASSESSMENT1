import pandas as pd

# Load dataset with similarities (from part d)
df = pd.read_csv("d_change_magnitude.csv")

# Semantic thresholds
df["Semantic_class"] = df["Semantic_Similarity"].apply(
    lambda x: "Minor" if x >= 0.80 else "Major"
)
# Token thresholds
df["Token_class"] = df["Token_Similarity"].apply(
    lambda x: "Minor" if x >= 0.75 else "Major"
)

# Agreement check
df["Classes_Agree"] = (df["Semantic_class"] == df["Token_class"]).map({True: "YES", False: "NO"})

# ---------------- Save Output ----------------
df.to_csv("e_classification.csv", index=False)
print("Classification & agreement saved to e_classification.csv")
