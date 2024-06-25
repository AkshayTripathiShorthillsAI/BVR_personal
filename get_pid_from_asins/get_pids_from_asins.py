import mysql.connector
import pandas as pd
import os
from datetime import datetime

# Load the Excel file
excel_file = "/home/shtlp0133/Deletion update/Pending scrapinng ASIN.xlsx"
df = pd.read_excel(excel_file)

# Get the unique category_slug and asin pairs
category_asin_pairs = df[['category_slug', 'asin']].drop_duplicates()

print("Number of unique category_slug + asin pairs:", len(category_asin_pairs))

def execute_query_and_save_results(category_asin_pairs, output_folder):
    # Get today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Create a batch folder
    # Check if a folder with the same date already exists
    batch_number = 1
    while True:
        batch_folder = os.path.join(output_folder, f"{today_date}_batch{batch_number}")
        if not os.path.exists(batch_folder):
            os.makedirs(batch_folder, exist_ok=True)
            break
        batch_number += 1

    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(
            host="velocity-production.mysql.database.azure.com",
            user="powerbi",
            password="h29@2iJ9",
            database="data_pipeline"
        )
        cursor = conn.cursor(dictionary=True)
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return

    # Collect all results in a single DataFrame
    all_data = []

    # Execute the query for each category + asin pair
    for index, row in category_asin_pairs.iterrows():
        category = row['category_slug']
        asin = row['asin']
        
        print(f"Executing query for category: '{category}', asin: '{asin}'")  # Debugging output

        try:
            cursor.execute("""
                SELECT
                    DISTINCT
                    dc.category_slug,
                    vp.asin,
                    vp.pid AS pid
                FROM
                    data_pipeline.velocity_product vp
                LEFT JOIN
                    data_pipeline.dataflow_category dc ON vp.category_id = dc.id
                WHERE
                    dc.category_slug = %s AND vp.asin = %s;
            """, (category, asin))
            rows = cursor.fetchall()

            if rows:
                all_data.extend(rows)
                print(f"Data found for category: '{category}', asin: '{asin}'")  # Debugging output
            else:
                print(f"No data found for category: '{category}', asin: '{asin}'")
        except mysql.connector.Error as err:
            print(f"Error executing query for category '{category}' and asin '{asin}':", err)

    # Close database connection
    cursor.close()
    conn.close()

    # Save all data to a single Excel file
    if all_data:
        df_all = pd.DataFrame(all_data)
        output_file = os.path.join(batch_folder, "reactivate_list.xlsx")
        df_all.to_excel(output_file, index=False)
        print(f"All data saved to {output_file}: Rows written: {len(df_all)}")
    else:
        print("No data found for any of the category + asin pairs")

# Example usage
output_folder = "reactivate_excels"
execute_query_and_save_results(category_asin_pairs, output_folder)