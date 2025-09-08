import pandas as pd
from pydriller import Repository
from transformers import T5ForConditionalGeneration, AutoTokenizer
import os
import torch

print("Libraries imported successfully.")


repo_path = os.path.join(os.getcwd(), 'browser-use')
input_csv_path = 'bug_fixing_commits.csv'
output_csv_path = 'llm_generated_messages.csv'


print("Loading the T5 model and tokenizer...")
model_name = "mamiksik/CommitPredictorT5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
print("Model loaded successfully.")


df_bugs = pd.read_csv(input_csv_path)




commit_hashes = df_bugs['Hash'].tolist()


detailed_commits_data = []

print(f"Starting analysis of {len(commit_hashes)} commits...")


for commit in Repository(repo_path, only_commits=commit_hashes).traverse_commits():
    
    for modified_file in commit.modified_files:
        
        diff_text = modified_file.diff
        source_before = modified_file.source_code_before
        source_current = modified_file.source_code
        filename = modified_file.new_path or modified_file.old_path

        if not diff_text:
            continue
            
        max_length = 512
        inputs = tokenizer.encode(
            "generate commit message: " + diff_text, 
            return_tensors="pt", 
            max_length=max_length, 
            truncation=True
        )
        
        outputs = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)
        llm_message = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        commit_info = {
            'Hash': commit.hash,
            'Message': commit.msg,
            'Filename': filename,
            'Source Code (before)': source_before,
            'Source Code (current)': source_current,
            'Diff': diff_text,
            'LLM Inference (fix type)': llm_message,
            'Rectified Message': ''
        }
        detailed_commits_data.append(commit_info)

    print(f"Processed commit {commit.hash} - Found {len(detailed_commits_data)} file diffs so far.")

print("\nFinished generating messages.")


df_detailed = pd.DataFrame(detailed_commits_data)


df_detailed.to_csv(output_csv_path, index=False)

print(f" data successfully saved to {output_csv_path}")