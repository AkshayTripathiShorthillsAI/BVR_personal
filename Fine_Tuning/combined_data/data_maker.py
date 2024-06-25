import os
import pandas as pd

def combine_csv_files(folder_path):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    combined_data_list = []
    
    for file in csv_files:
        category_name = os.path.splitext(file)[0]
        
        df = pd.read_csv(os.path.join(folder_path, file))
        
        df = df[df['accept_choice1'] == 'YES']
        
        df['category_name'] = category_name
        
        combined_data_list.append(df)
    
    combined_data = pd.concat(combined_data_list, ignore_index=True)
    
    combined_data.to_csv('combined_data.csv', index=False)
    print("Combined CSV file saved as 'combined_data.csv'.")

# Specify the folder path containing the CSV files
folder_path = '/home/shtlp_0015/Desktop/BVR/Fine_Tuning/combined_data/fine_tuning_dataset_input'

# Call the function to combine CSV files
combine_csv_files(folder_path)
