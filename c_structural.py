import pandas as pd
from radon.metrics import mi_visit
from radon.complexity import cc_visit
from radon.raw import analyze

# Load dataset
df = pd.read_csv("evaluation_sample.csv")

# ---- Functions to compute metrics ----
def get_mi(code):
    try:
        return mi_visit(str(code), True)[0].mi
    except:
        return None

def get_cc(code):
    try:
        results = cc_visit(str(code))
        return sum(r.complexity for r in results) / max(1, len(results))
    except:
        return None

def get_loc(code):
    try:
        return analyze(str(code)).loc
    except:
        return None

# ---- Apply metrics ----
df["MI_Before"] = df["Source Code (before)"].apply(get_mi)
df["MI_After"]  = df["Source Code (current)"].apply(get_mi)

df["CC_Before"] = df["Source Code (before)"].apply(get_cc)
df["CC_After"]  = df["Source Code (current)"].apply(get_cc)

df["LOC_Before"] = df["Source Code (before)"].apply(get_loc)
df["LOC_After"]  = df["Source Code (current)"].apply(get_loc)

# ---- Compute changes ----
df["MI_Change"]  = df["MI_After"] - df["MI_Before"]
df["CC_Change"]  = df["CC_After"] - df["CC_Before"]
df["LOC_Change"] = df["LOC_After"] - df["LOC_Before"]

# ---- Save output ----
df.to_csv("c_structural.csv", index=False)
print("Structural metrics saved to c_structural.csv")
