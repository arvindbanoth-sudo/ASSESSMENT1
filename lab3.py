import pandas as pd
from radon.metrics import mi_visit
from radon.complexity import cc_visit
from radon.raw import analyze
from transformers import RobertaTokenizer, RobertaModel
import torch
import sacrebleu
from torch.nn import functional as F

df = pd.read_csv("evaluation_sample.csv")

print("\n===== Baseline Stats =====")
print("Total commits:", df["Hash"].nunique())
print("Total files:", len(df))
print("Average modified files per commit:", df.groupby("Hash")["Filename"].count().mean())

print("\nFix type distribution:\n", df["LLM Inference (fix type)"].value_counts())
print("\nMost frequent extensions:\n", df["Filename"].str.split(".").str[-1].value_counts().head())

def get_mi(code):
    try:
        return mi_visit(code, True)[0].mi
    except:
        return None

def get_cc(code):
    try:
        results = cc_visit(code)
        return sum(r.complexity for r in results) / max(1, len(results))
    except:
        return None

def get_loc(code):
    try:
        return analyze(code).loc
    except:
        return None

df["MI_Before"] = df["Source Code (before)"].apply(get_mi)
df["MI_After"]  = df["Source Code (current)"].apply(get_mi)
df["CC_Before"] = df["Source Code (before)"].apply(get_cc)
df["CC_After"]  = df["Source Code (current)"].apply(get_cc)
df["LOC_Before"] = df["Source Code (before)"].apply(get_loc)
df["LOC_After"]  = df["Source Code (current)"].apply(get_loc)

df["MI_Change"]  = df["MI_After"] - df["MI_Before"]
df["CC_Change"]  = df["CC_After"] - df["CC_Before"]
df["LOC_Change"] = df["LOC_After"] - df["LOC_Before"]


print("\nLoading CodeBERT (this may take ~1 minute on first run)...")
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaModel.from_pretrained("microsoft/codebert-base")

def get_embedding(text):
    inputs = tokenizer(str(text), return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze()

def semantic_similarity(code1, code2):
    v1, v2 = get_embedding(code1), get_embedding(code2)
    return F.cosine_similarity(v1.unsqueeze(0), v2.unsqueeze(0)).item()

df["Semantic_Similarity"] = df.apply(
    lambda row: semantic_similarity(row["Source Code (before)"], row["Source Code (current)"]),
    axis=1
)


def bleu_score(before, after):
    return sacrebleu.sentence_bleu(str(after), [str(before)]).score / 100

df["Token_Similarity"] = df.apply(
    lambda row: bleu_score(row["Source Code (before)"], row["Source Code (current)"]),
    axis=1
)


df["Semantic_class"] = df["Semantic_Similarity"].apply(lambda x: "Minor" if x >= 0.80 else "Major")
df["Token_class"] = df["Token_Similarity"].apply(lambda x: "Minor" if x >= 0.75 else "Major")
df["Classes_Agree"] = (df["Semantic_class"] == df["Token_class"]).map({True: "YES", False: "NO"})


df.to_csv("lab3_output.csv", index=False)
print("\n Analysis complete! Results saved in lab3_output.csv")
