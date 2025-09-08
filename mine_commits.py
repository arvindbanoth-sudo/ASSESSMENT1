import pandas as pd
from pydriller import Repository
import os


repo_path = os.path.join(os.getcwd(), 'browser-use')


BUG_FIX_KEYWORDS = ['fix', 'bug', 'defect', 'patch', 'error', 'repair', 'correct']

bug_commits_data = []

print(f"Starting to mine repository at: {repo_path}")

for commit in Repository(repo_path).traverse_commits():
    
 
    commit_message_lower = commit.msg.lower()
    if any(keyword in commit_message_lower for keyword in BUG_FIX_KEYWORDS):
        commit_hash = commit.hash
        commit_message = commit.msg
        
        parent_hashes = commit.parents
        is_merge = commit.merge
        modified_files = [f.new_path or f.old_path for f in commit.modified_files]

        
        commit_info = {
            'Hash': commit_hash,
            'Message': commit_message,
            'Hashes of parents': parent_hashes,
            'Is a merge commit?': is_merge,
            'List of modified files': modified_files
        }
        
       
        bug_commits_data.append(commit_info)

        
        if len(bug_commits_data) % 50 == 0:
            print(f"Found {len(bug_commits_data)} bug-fixing commits so far...")

print(f"\nFinished mining. Found a total of {len(bug_commits_data)} bug-fixing commits.")


df = pd.DataFrame(bug_commits_data)
output_filename = 'bug_fixing_commits.csv'
df.to_csv(output_filename, index=False)

print(f" Data successfully saved to {output_filename}")