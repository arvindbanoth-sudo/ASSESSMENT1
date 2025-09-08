import pandas as pd


final_data_path = 'final_report_data.csv'


print("Calculating final results from the combined data...")

try:

    eval_df = pd.read_csv(final_data_path)

    
    required_columns = ['is_developer_precise', 'is_llm_precise', 'is_rectifier_precise']
    if not all(col in eval_df.columns for col in required_columns):
        print("Error: The CSV file is missing one of the required classification columns.")
    else:
       
        dev_hit_rate = eval_df['is_developer_precise'].mean() * 100

    
        llm_hit_rate = eval_df['is_llm_precise'].mean() * 100

        
        rectifier_hit_rate = eval_df['is_rectifier_precise'].mean() * 100

        print("\n--- Evaluation Results ---")
        print(f"RQ1 - Developer Precision Hit Rate: {dev_hit_rate:.2f}%")
        print(f"RQ2 - Raw LLM Precision Hit Rate:   {llm_hit_rate:.2f}%")
        print(f"RQ3 - Rectified LLM Precision Hit Rate: {rectifier_hit_rate:.2f}%")
        print("--------------------------\n")

except FileNotFoundError:
    print(f"Error: Could not find the file '{final_data_path}'. Please make sure it exists.")
