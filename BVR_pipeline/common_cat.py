import pandas as pd

# Paths to your Excel files
file1 = '/home/shtlp_0170/Desktop/BVR/BVR_pipeline/Golden set - events.xlsx'
file2 = '/home/shtlp_0170/Desktop/BVR/BVR_pipeline/GS 2024 Content Team (1).xlsx'

# Read the Excel files
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# Print column names for debugging
print("Columns in first Excel file:", df1.columns)
print("Columns in second Excel file:", df2.columns)

# Extract 'category_slug' columns with error handling
try:
    category_slug_1 = df1['category_slug']
except KeyError:
    raise KeyError("Column 'category_slug' not found in the first Excel file")

try:
    category_slug_2 = df2['Category Slug']
except KeyError:
    raise KeyError("Column 'Category Slug' not found in the second Excel file")

# Convert to string for reliable comparison if needed
category_slug_1 = category_slug_1.astype(str)
category_slug_2 = category_slug_2.astype(str)

# Find common values
common_values = set(category_slug_1).intersection(set(category_slug_2))

# Print the number of common categories found
print(f"Number of common categories found: {len(common_values)}")

# Convert the common values to a DataFrame
common_values_df = pd.DataFrame(list(common_values), columns=['category_slug'])

# Optionally, save to a new Excel file
output_file = 'common_category_slug.xlsx'
common_values_df.to_excel(output_file, index=False)

print(f"Common values saved to {output_file}")