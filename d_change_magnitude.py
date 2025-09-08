import pandas as pd
from transformers import RobertaTokenizer, RobertaModel
import torch
from torch.nn import functional as F
import sacrebleu

# Load dataset
df = pd.read_csv("evaluation_sample.csv")
print("\nLoading CodeBERT (first run may take ~1 min)...")
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

# ---------------- Token Similarity (BLEU) ----------------
def bleu_score(before, after):
    return sacrebleu.sentence_bleu(str(after), [str(before)]).score / 100

df["Token_Similarity"] = df.apply(
    lambda row: bleu_score(row["Source Code (before)"], row["Source Code (current)"]),
    axis=1
)
df.to_csv("d_change_magnitude.csv", index=False)
print(" Change magnitude metrics saved to d_change_magnitude.csv")
