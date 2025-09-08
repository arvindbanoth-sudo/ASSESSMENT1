import pandas as pd
import re 

def rectify_message(row):
    llm_message = row['LLM Inference (fix type)']
    diff = row['Diff']
    filename = row['Filename']
    
    new_message = llm_message 
    # Rule 1: Add function name if the message is generic
    if "fix" in llm_message.lower() and len(llm_message.split()) < 3:
        
        match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', diff)
        if match:
            function_name = match.group(1)
            new_message = f"Fix: Update function `{function_name}`"

    # Rule 2: Add context about null checks
    if "is None" in diff or "== null" in diff:
        # Make sure we don't add the phrase if it's already there
        if "null check" not in new_message:
            new_message = new_message + " by adding a null check"
            
    # Rule 3: Add context for test files
    if 'test' in filename.lower():
        if "[Test]" not in new_message:
            new_message = "[Test] " + new_message

   
    return new_message


print("Starting the rectification process...")


df = pd.read_csv('llm_generated_messages.csv')


df['Rectified Message'] = df.apply(rectify_message, axis=1)


output_filename = 'final_analyzed_data.csv'
df.to_csv(output_filename, index=False)

print(f" Rectification complete. Final data saved to {output_filename}")