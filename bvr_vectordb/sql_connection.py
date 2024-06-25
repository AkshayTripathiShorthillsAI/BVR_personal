import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

csv_file_path = os.getenv("DATASET_PATH")
output_csv_file_path = os.getenv("FILE_PATH_CSV")

df = pd.read_csv(csv_file_path)

product_data = zip(df['category_slug'], df['ASIN'])

conn = mysql.connector.connect(
    user= 'powerbi',
    password= 'h29@2iJ9',
    host= 'velocity-production.mysql.database.azure.com',
    database= 'data_pipeline'
)

cursor = conn.cursor()

final_data = []

for category_slug, asin in product_data:
    cursor.execute("""SELECT dc.category_slug, p.pid, p.product_slug, p.json_file, p.asin, p.updated_at
                      FROM data_pipeline.dataflow_category dc
                      LEFT JOIN data_pipeline.velocity_product p
                      ON p.category_id = dc.id
                      WHERE dc.category_slug = %s AND p.asin = %s""" , (category_slug, asin))

    result = cursor.fetchone()  # Since combination is unique, fetchone is sufficient
    print(result)
    if result:
        final_data.append(result)

final_df = pd.DataFrame(final_data, columns=['category_slug', 'pid', 'product_slug', 'json_file', 'asin', 'updated_at'])

final_df.to_csv(output_csv_file_path, index=False)

cursor.close()
conn.close()
