"""
compare_diff_algos.py
Compares git diffs from two algorithms (myers & histogram) for multiple repos.
Generates a CSV with columns:
repo,old_file_path,new_file_path,commit_SHA,parent_SHA,commit_message,diff_myers,diff_hist,Discrepancy,file_type
"""

import os
import re
import subprocess
from pathlib import Path
from pydriller import Repository

import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

REPO_PATHS = [
    str(Path.home() / "Desktop/CS202-Lab4/repos/adk-python"),
    str(Path.home() / "Desktop/CS202-Lab4/repos/verl"),
    str(Path.home() / "Desktop/CS202-Lab4/repos/yoloe")
]
OUTPUT_CSV = str(Path.home() / "Desktop/CS202-Lab4/outputs/diff_comparison_allrepos.csv")
PLOT_PATH = str(Path.home() / "Desktop/CS202-Lab4/plots/mismatches_by_filetype.png")

def run_git_diff(repo_path, parent_sha, commit_sha, filepath, algorithm):
    cmd = [
        "git", "diff",
        f"--diff-algorithm={algorithm}",
        "-w",  # ignore all whitespace
        "-B",  # ignore blank lines
        parent_sha, commit_sha, "--", filepath
    ]
    try:
        proc = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=False)
        return proc.stdout
    except Exception as e:
        print(f"Error running git diff: {e} - cmd: {' '.join(cmd)}")
        return ""

def normalize_diff(diff_text):
    normalized = []
    for line in diff_text.splitlines():
        if line.startswith(("diff ", "index ", "--- ", "+++ ", "@@")):
            continue
        if not line:
            continue
        sign = line[0]
        if sign not in ("+", "-", " "):
            continue
        content = line[1:]
        content_nospace = re.sub(r"\s+", "", content)
        if content_nospace == "":
            continue
        normalized.append(f"{sign}{content_nospace}")
    return "\n".join(normalized)

def classify_file_type(path):
    p = path.lower()
    name = os.path.basename(p)
    ext = os.path.splitext(name)[1]
    if name in ("readme", "readme.md", "readme.rst", "readme.txt"):
        return "README"
    if name.startswith("license") or name == "license" or name.startswith("copying"):
        return "LICENSE"
    if "/test/" in p or "/tests/" in p or name.startswith("test_") or name.endswith("_test.py") or "spec" in p:
        return "TEST"
    if ext in (".py", ".java", ".c", ".cpp", ".h", ".js", ".ts", ".go", ".rb", ".cs"):
        return "SOURCE"
    return "OTHER"

rows = []

for repo in REPO_PATHS:
    if not os.path.isdir(repo):
        print(f"Repo path not found: {repo} - skipping")
        continue

    print(f"Mining repo: {repo}")
    for commit in tqdm(Repository(repo).traverse_commits(), desc=os.path.basename(repo)):
        if len(commit.parents) != 1:
            continue
        parent_sha = commit.parents[0]
        commit_sha = commit.hash
        commit_msg = commit.msg.replace("\n", " ").strip()

        for mod in commit.modified_files:
            old_path = mod.old_path if mod.old_path else ""
            new_path = mod.new_path if mod.new_path else ""
            file_to_check = new_path or old_path
            if not file_to_check:
                continue

            diff_myers = run_git_diff(repo, parent_sha, commit_sha, file_to_check, "myers")
            diff_hist = run_git_diff(repo, parent_sha, commit_sha, file_to_check, "histogram")

            norm_myers = normalize_diff(diff_myers)
            norm_hist = normalize_diff(diff_hist)

            discrepancy = "Yes" if norm_myers != norm_hist else "No"

            rows.append({
                "repo": os.path.basename(repo),
                "old_file_path": old_path,
                "new_file_path": new_path,
                "commit_SHA": commit_sha,
                "parent_SHA": parent_sha,
                "commit_message": commit_msg,
                "diff_myers": diff_myers,
                "diff_hist": diff_hist,
                "Discrepancy": discrepancy,
                "file_type": classify_file_type(file_to_check)
            })


os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Wrote {len(df)} rows to {OUTPUT_CSV}")


mismatch_counts = df[df["Discrepancy"] == "Yes"].groupby("file_type").size().reset_index(name="mismatches")
plt.figure(figsize=(8,5))
plt.bar(mismatch_counts["file_type"], mismatch_counts["mismatches"])
plt.title("Mismatches (Myers vs Histogram) by file type")
plt.xlabel("File type")
plt.ylabel("Number of mismatches")
plt.tight_layout()
os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)
plt.savefig(PLOT_PATH)
print(f"Saved plot to {PLOT_PATH}")
