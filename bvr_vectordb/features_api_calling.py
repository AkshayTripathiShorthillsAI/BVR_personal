import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()

output_file = os.getenv("FEATURES_OUTPUT_FILE")
api_url_template = os.getenv("FEATURES_API_URL")
api_key = os.getenv("FEATURES_API_KEY")
input_csv_file = "/home/shtlp_0015/Desktop/BVR/bvr_vectordb/dataset_2024-05-29_batch_2.csv" 
print(input_csv_file)

# Set headers including Authorization header with API key
headers = {'Authorization': f'Token {api_key}'}

# Function to make API call for a given category_slug
def make_api_call(category_slug):
    url = api_url_template+category_slug
    print(url)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred for category_slug {category_slug}: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred for category_slug {category_slug}: {err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for category_slug {category_slug}: {e}")
        return None

# Read category_slugs from input CSV file
try:
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        category_slugs = set(row['category_slug'] for row in reader)
        # category_slugs = {"bark-collars"}
except FileNotFoundError:
    print("Input CSV file not found.")
    category_slugs = []

# Make API calls for each unique category_slug
data = []
for category_slug in category_slugs:
    api_response = make_api_call(category_slug)
    features = list(api_response['features'].keys())
    print(features)
    if api_response:
        # data.append({'category_slug': category_slug, 'features': api_response['features']})
        for feature in features:
            data.append({'category_slug':category_slug,'features':feature,'query':feature})

# Writing the data to a CSV file
if data:
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['category_slug', 'features','query']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data written to {output_file}")
    except Exception as e:
        print(f"An error occurred while writing data to CSV: {e}")
else:
    print("No data to write.")

