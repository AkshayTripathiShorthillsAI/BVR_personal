# import pandas as pd

# # Define the path to your CSV file
# # csv_path = '/home/shtlp_0170/Desktop/BVR/Annotation/round-ring-binders.csv'
# # csv_path = "/home/shtlp_0170/Desktop/BVR/Annotation/project-folders.csv"
# csv_path = "/home/shtlp_0170/Desktop/BVR/Annotation/wooden_color_pencils.csv"
# csv_path = "/home/shtlp_0170/Desktop/BVR/Annotation/bento-boxes.csv"
# # Optional: Define a new path if you want to save the updated CSV as a new file
# # new_csv_path = '/home/shtlp_0170/Desktop/BVR/Annotation/round-ring-binders-updated.csv'

# try:
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv(csv_path)
    
#     # Ensure the columns 'accept_choice1' and 'Model_choice' exist
#     if 'accept_choice1' in df.columns and 'Model_choice' in df.columns:
        
#         # Create a new column 'compare' to indicate if the values are same or different
#         df['compare'] = df.apply(lambda row: 'same' if row['accept_choice1'] == row['Model_choice'] else 'different', axis=1)
        
#         # Calculate the percentage of 'NO' values that are the same
#         no_values = df[(df['accept_choice1'] == 'NO')]
#         no_same = no_values[no_values['compare'] == 'same']
#         percentage_no_same = (len(no_same) / len(no_values)) * 100 if len(no_values) > 0 else 0
        
#         # Count how many 'YES', 'NO', 'OTHER' are 'different'
#         count_different = df[df['compare'] == 'different']['accept_choice1'].value_counts()
#         yes_diff = count_different.get('YES', 0)
#         no_diff = count_different.get('NO', 0)
#         other_diff = count_different.get('OTHER', 0)
        
#         # Save the updated DataFrame back to the CSV file
#         df.to_csv(csv_path, index=False)
        
#         # Optionally save to a new CSV file
#         # df.to_csv(new_csv_path, index=False)
        
#         # Print the updated DataFrame and the percentage
#         print(df)
#         print(f"Percentage of 'NO' values that are the same: {percentage_no_same:.2f}%")
#         print(f"Count of 'YES' that are different: {yes_diff}")
#         print(f"Count of 'NO' that are different: {no_diff}")
#         print(f"Count of 'OTHER' that are different: {other_diff}")
        
#     else:
#         print("Columns 'accept_choice1' and 'Model_choice' not found in the CSV file.")
# except FileNotFoundError:
#     print(f"File not found: {csv_path}")
# except pd.errors.EmptyDataError:
#     print("CSV file is empty.")
# except Exception as e:
#     print(f"An error occurred: {e}")


import pandas as pd

# Define the path to your CSV file
# csv_path = '/home/shtlp_0170/Desktop/BVR/Annotation/round-ring-binders.csv'
# csv_path = "/home/shtlp_0170/Desktop/BVR/Annotation/project-folders.csv"
csv_path = "/home/shtlp_0170/Desktop/BVR/Annotation/wooden_color_pencils.csv"
# csv_path = "/home/shtlp_0170/Desktop/BVR/Annotation/bento-boxes.csv"
# Optional: Define a new path if you want to save the updated CSV as a new file
# new_csv_path = '/home/shtlp_0170/Desktop/BVR/Annotation/round-ring-binders-updated.csv'

try:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Ensure the columns 'accept_choice1' and 'Model_choice' exist
    if 'accept_choice1' in df.columns and 'Model_choice' in df.columns:
        
        # Create a new column 'compare' to indicate if the values are same or different
        df['compare'] = df.apply(lambda row: 'same' if row['accept_choice1'] == row['Model_choice'] else 'different', axis=1)
        
        # Filter 'YES', 'NO', 'OTHER' values and count differences
        yes_values = df[(df['accept_choice1'] == 'YES')]
        yes_diff = yes_values[yes_values['compare'] == 'different']
        percentage_yes_diff = (len(yes_diff) / len(yes_values)) * 100 if len(yes_values) > 0 else 0
        
        no_values = df[(df['accept_choice1'] == 'NO')]
        no_diff = no_values[no_values['compare'] == 'different']
        percentage_no_same = (len(no_values) - len(no_diff)) / len(no_values) * 100 if len(no_values) > 0 else 0
        
        other_values = df[(df['accept_choice1'] == 'OTHER')]
        other_diff = other_values[other_values['compare'] == 'different']
        
        # Save the updated DataFrame back to the CSV file
        df.to_csv(csv_path, index=False)
        
        # Optionally save to a new CSV file
        # df.to_csv(new_csv_path, index=False)
        
        # Print the updated DataFrame and the results
        print(df)
        print(f"Percentage of 'NO' values that are the same: {percentage_no_same:.2f}%")
        print(f"Count of 'YES' that are different: {len(yes_diff)}")
        print(f"Count of 'NO' that are different: {len(no_diff)}")
        print(f"Count of 'OTHER' that are different: {len(other_diff)}")
        print(f"Percentage of 'YES' values that are different: {percentage_yes_diff:.2f}%")
        
    else:
        print("Columns 'accept_choice1' and 'Model_choice' not found in the CSV file.")
except FileNotFoundError:
    print(f"File not found: {csv_path}")
except pd.errors.EmptyDataError:
    print("CSV file is empty.")
except Exception as e:
    print(f"An error occurred: {e}")
