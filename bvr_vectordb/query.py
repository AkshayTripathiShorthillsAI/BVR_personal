import weaviate
import json
import csv
import os
import pandas as pd
from collections import defaultdict
from sentence_transformers import SentenceTransformer, CrossEncoder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Weaviate Authentication
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_AUTH_KEY = os.getenv("WEAVIATE_AUTH_KEY")

WEAVIATE_CLASS_NAME = "Product_Details_FOR_SNIPPETS"
BATCH_SIZE = 50
WORKERS_COUNT = 10

LIMIT_FOR_QUERY_RESPONSE = 200
LIMIT_FOR_RERANKING_MODEL = 30
LIMIT_FOR_FINAL_OUTPUT = 8
FILE_FOR_COLUMN_NAMES = os.getenv("FILE_FOR_COLUMN_NAMES")
FEATURES_CSV = os.getenv("FEATURES_CSV")
DUMPING_FOLDER = os.getenv("DUMPING_FOLDER_FILTERED_FEATURES")

# Column names to access
THINGS_TO_ACCESS = pd.read_excel(FILE_FOR_COLUMN_NAMES)["columnNames"].tolist()

# Model used for vector encoding
MODEL = SentenceTransformer('thenlper/gte-large')

# Load PIDs and categories
PIDS_FILE = os.getenv("FILE_PATH_CSV")
df_pid = pd.read_csv(PIDS_FILE)
CATEGORY = df_pid['category_slug'].unique()

# Empty batch_callback function
def batch_callback(callback):
    pass

# Getting CLIENT
def get_client():
    auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_AUTH_KEY)
    client = weaviate.Client(url=WEAVIATE_URL, auth_client_secret=auth_config)
    client.batch.configure(batch_size=BATCH_SIZE, callback=batch_callback, num_workers=WORKERS_COUNT)
    return client

# CLIENT
CLIENT = get_client()

# Reranking Function
crs_end_model_card = "cross-encoder/ms-marco-MiniLM-L-12-v2"
CROSS_ENC_MODEL = CrossEncoder(crs_end_model_card, device='cpu')

def rerank_results(query, df):
    pairs = [[query, tx] for tx in df["chunkedData"]]
    cross_scores = list(CROSS_ENC_MODEL.predict(pairs))
    df["score"] = cross_scores
    df = df.sort_values('score', ascending=False)
    return df

# Loading csv files
ASPECTS_DF = pd.read_csv(FEATURES_CSV)

# Dictionary to store responses
responses = {}

for category in CATEGORY:
    LIST_OF_PIDS = list(df_pid[df_pid["category_slug"] == category]["pid"])
    aspects = list(ASPECTS_DF[ASPECTS_DF["category_slug"] == category]["features"])
    queries = list(ASPECTS_DF[ASPECTS_DF["category_slug"] == category]["query"])
    aspect_to_query = {aspect: str(query) for aspect, query in zip(aspects, queries)}
    
    print("Querying for category: " + str(category))
    print("These all products will be queried", LIST_OF_PIDS)
    
    category_folder = os.path.join(DUMPING_FOLDER, category)
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)
        print(f"Directory '{category_folder}' created.")
    else:
        print(f"Directory '{category_folder}' already exists.")

    for pid in LIST_OF_PIDS:
        combined_data_frame = pd.DataFrame()
        combined_data = {}

        for aspect, query in aspect_to_query.items():
            try:
                response = (
                    CLIENT.query
                    .get(WEAVIATE_CLASS_NAME, THINGS_TO_ACCESS)
                    .with_near_vector({
                        "vector": MODEL.encode(query).tolist(),
                        "certainty": 0.8  # Adjusted certainty threshold
                    })
                    .with_additional(["distance"])
                    .with_limit(LIMIT_FOR_QUERY_RESPONSE)
                    .with_where({
                        "path": ["pid"],
                        "operator": "Equal",
                        "valueText": pid
                    })
                    .do()
                )
                print(f"Response for PID {pid}, Aspect {aspect}: {response}")
                df = pd.DataFrame(response['data']["Get"][WEAVIATE_CLASS_NAME])
                
                if df.empty:
                    print(f"No data found for pid {pid} for query {query}")
                    continue
                
                reranked_df = rerank_results(query, df.head(LIMIT_FOR_RERANKING_MODEL))
                reranked_df = reranked_df.head(LIMIT_FOR_FINAL_OUTPUT)
                reranked_df.to_csv("pid_1.csv")

                column_to_count = "reviewText"
                reranked_df['frequency'] = reranked_df.groupby(column_to_count)[column_to_count].transform('count')
                reranked_df.to_excel("pid1.xlsx")
                reranked_df['pid'] = pid
                reranked_df['aspect'] = aspect
                reranked_df['query'] = query
                reranked_df['openAiText'] = reranked_df.apply(lambda row: row['chunkedData'] if row['frequency'] == 1 else row['reviewText'], axis=1)
                reranked_df = reranked_df[~reranked_df.duplicated(subset=['openAiText'], keep='first')]
                combined_data_frame = pd.concat([combined_data_frame, reranked_df], ignore_index=True)
                
                # Store combined data for this aspect
                combined_data[aspect] = response['data']["Get"][WEAVIATE_CLASS_NAME]

            except Exception as e:
                print(f"An error occurred for PID {pid} with aspect {aspect}: {e}")
                continue

        # Save combined data for this PID in the responses dictionary
        responses[pid] = combined_data

        # Save to Excel file
        xlsx_file = os.path.join(category_folder, f"{pid}.xlsx")
        if not combined_data_frame.empty:
            combined_data_frame.to_excel(xlsx_file, index=False)
            print(f"Saved data for PID {pid} to {xlsx_file}")

# Write all responses to a JSON file
with open('pid.json', 'w') as json_file:
    json.dump(responses, json_file, indent=4)
    print("All responses saved to 'pid.json'")


# import weaviate
# import json
# import csv
# import os
# import pandas as pd
# from collections import defaultdict
# from sentence_transformers import SentenceTransformer, CrossEncoder
# from dotenv import load_dotenv
# load_dotenv()

# # Weaviate Authentication
# WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
# WEAVIATE_AUTH_KEY = os.getenv("WEAVIATE_AUTH_KEY")

# WEAVIATE_CLASS_NAME = "Product_Details_FOR_SNIPPETS"
# BATCH_SIZE = 50
# WORKERS_COUNT = 10

# LIMIT_FOR_QUERY_RESPONSE = 200
# LIMIT_FOR_RERANKING_MODEL = 30
# LIMIT_FOR_FINAL_OUTPUT = 8
# FILE_FOR_COLUMN_NAMES = os.getenv("FILE_FOR_COLUMN_NAMES")

# FEATURES_CSV = os.getenv("FEATURES_CSV")    # Features/aspects csv file

# DUMPING_FOLDER = os.getenv("DUMPING_FOLDER_FILTERED_FEATURES")   # Dumping folder of filtered features

# # ["reviewerName","reviewerUrl","rating","reviewTitle","reviewDate","reviewText","is_Helpful","unique_column","textLength","chunkedData","category"]
# THINGS_TO_ACCESS = pd.read_excel(FILE_FOR_COLUMN_NAMES)["columnNames"].tolist() 

# # Model used in vector encoding
# MODEL = SentenceTransformer('thenlper/gte-large')

# # File containing PIDs of files to be uploaded
# PIDS_FILE = os.getenv("FILE_PATH_CSV")   # PID CSV FILE PATH
# df_pid = pd.read_csv(PIDS_FILE)

# # All categories
# CATEGORY = df_pid['category_slug'].unique()

# # Just empty batch_callback function
# def batch_callback(callback):
#     # print(callback)
#     pass

# # Getting CLIENT
# def get_client():
#     auth_config = weaviate.auth.AuthApiKey(api_key=WEAVIATE_AUTH_KEY)
    
#     client = weaviate.Client(
#         url=WEAVIATE_URL,
#         auth_client_secret=auth_config
#     )
    
#     client.batch.configure(batch_size=BATCH_SIZE, callback=batch_callback, num_workers=WORKERS_COUNT)  # Configure batch
#     return client

# # CLIENT
# CLIENT = get_client()

# # Reranking Function
# crs_end_model_card = "cross-encoder/ms-marco-MiniLM-L-12-v2"
# CROSS_ENC_MODEL = CrossEncoder(crs_end_model_card, device='cpu')

# def rerank_results(query, df):
#     a = [[query, tx] for tx in df["chunkedData"]]
#     cross_scores = list(CROSS_ENC_MODEL.predict(a))
#     df["score"] = cross_scores
#     df = df.sort_values('score', ascending=False)
#     return df

# # Loading csv files
# ASPECTS_DF = pd.read_csv(FEATURES_CSV)

# for category in CATEGORY:

#     LIST_OF_PIDS = list(df_pid[df_pid["category_slug"] == category]["pid"])
#     aspects = list(ASPECTS_DF[ASPECTS_DF["category_slug"] == category]["features"])
#     queries = list(ASPECTS_DF[ASPECTS_DF["category_slug"] == category]["query"])
#     aspect_to_query = {aspect: str(query) for aspect, query in zip(aspects, queries)}
    
#     print("Querying for category: " + str(category))
#     print("These all products will be queried", LIST_OF_PIDS)
    
#     if not os.path.exists(DUMPING_FOLDER + "/" + category):
#         # If it doesn't exist, create the directory
#         os.makedirs(DUMPING_FOLDER + "/" + category)
#         print(f"Directory '{DUMPING_FOLDER}/{category}' created.")
#     else:
#         print(f"Directory '{DUMPING_FOLDER}/{category}' already exists.")

#     for pid in LIST_OF_PIDS:
#         combined_data_frame = pd.DataFrame()
#         # For different naming of features
#         for aspect, query in aspect_to_query.items():
#             try:   
#                 response = (
#                     CLIENT.query
#                     .get(WEAVIATE_CLASS_NAME, THINGS_TO_ACCESS)
#                     .with_near_vector({
#                         "vector": MODEL.encode(query).tolist(),
#                         "certainty": 0.885
#                     })
#                     .with_additional(["distance"])
#                     .with_limit(LIMIT_FOR_QUERY_RESPONSE)
#                     .with_where({
#                         "path": ["pid"],
#                         "operator": "Equal",
#                         "valueText": pid
#                     })
#                     .do()
#                 )
#                 # Using only the ones with minimum character length of character_limit_for_review and at max of limit_for_reranking_model
#                 cur_length = 0
#                 print(response)
#                 # Loading our data into dataFrame
#                 df = pd.DataFrame(response['data']["Get"][WEAVIATE_CLASS_NAME])
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 continue

#             if df.empty:
#                 print("No data found for pid " + pid + " for query " + query)
#                 continue
            
#             # Reanking the scores before dumping and pick up only up to size of limit_for_final_output
#             reranked_df = rerank_results(query, df.head(LIMIT_FOR_RERANKING_MODEL))

#             # Pick only some top values after reranking
#             reranked_df = reranked_df.head(LIMIT_FOR_FINAL_OUTPUT)

#             # Counting frequency of a row for which review length repeats and appending that frequency to our dataframe
#             column_to_count = "reviewText"

#             reranked_df['frequency'] = reranked_df.groupby(column_to_count)[column_to_count].transform('count')
#             reranked_df['pid'] = pid
#             reranked_df['aspect'] = aspect
#             reranked_df['query'] = query

#             # Picking the text which will go to OpenAi
#             reranked_df['openAiText'] = reranked_df.apply(lambda row: row['chunkedData'] if row['frequency'] == 1 else row['reviewText'], axis=1)

#             value_counts = reranked_df['openAiText'].value_counts()

#             # Dropping multiple instances
#             reranked_df = reranked_df[~reranked_df.duplicated(subset=['openAiText'], keep='first')]

#             combined_data_frame = pd.concat([combined_data_frame, reranked_df], ignore_index=True)

#         xlsx_file = DUMPING_FOLDER + "/" + category + "/" + pid + ".xlsx"

#         if not combined_data_frame.empty:
#             combined_data_frame.to_excel(xlsx_file, index=False)



# # Continue this tomorrow
# import weaviate
# import json
# import csv
# import os
# import pandas as pd
# from collections import defaultdict
# from sentence_transformers import SentenceTransformer, CrossEncoder
# from dotenv import load_dotenv
# load_dotenv()


# # Weaviate Authentication
# WEAVIATE_URL = os.getenv("WEAVIATE_URL")
# WEAVIATE_AUTH_KEY = os.getenv("WEAVIATE_AUTH_KEY")

# WEAVIATE_CLASS_NAME = "Product_Details_FOR_SNIPPETS"
# BATCH_SIZE = 50
# WORKERS_COUNT = 10


# LIMIT_FOR_QUERY_RESPONSE = 200
# LIMIT_FOR_RERANKING_MODEL = 30
# LIMIT_FOR_FINAL_OUTPUT = 8
# FILE_FOR_COLUMN_NAMES = os.getenv("FILE_FOR_COLUMN_NAMES")


# FEATURES_CSV = os.getenv("FEATURES_CSV")    # Features/aspects csv file

# DUMPING_FOLDER = os.getenv("DUMPING_FOLDER_FILTERED_FEATURES")   # Dumping folder of filtered features

# #["reviewerName","reviewerUrl","rating","reviewTitle","reviewDate","reviewText","is_Helpful","unique_column","textLength","chunkedData","category"]
# THINGS_TO_ACCESS = pd.read_excel(FILE_FOR_COLUMN_NAMES)["columnNames"].tolist() 


# # Model used in vector encoding
# MODEL = SentenceTransformer('thenlper/gte-large')

# # File containg pids of files to be uploaded
# PIDS_FILE = os.getenv("FILE_PATH_CSV")   # PID CSV FILE PATH
# df_pid = pd.read_csv(PIDS_FILE)

# # All categories
# CATEGORY = df_pid['category_slug'].unique()

# # Just empty batch_callback function
# def batch_callback(callback):
#     #print(callback)
#     pass


# # Getting CLIENT
# def get_client():
#     auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_AUTH_KEY)
 
#     client = weaviate.Client(
#         url=WEAVIATE_URL,
#         auth_client_secret=auth_config
#         )
    
#     client.batch.configure(batch_size=BATCH_SIZE,callback=batch_callback, num_workers=WORKERS_COUNT)  # Configure batch
#     return client

# # CLIENT
# CLIENT = get_client()

# # Reranking Function
# crs_end_model_card = "cross-encoder/ms-marco-MiniLM-L-12-v2"
# CROSS_ENC_MODEL = CrossEncoder(crs_end_model_card, device='cpu')

# def rerank_results(query, df):
#     a = [[query,tx] for tx in df["chunkedData"]]
#     cross_scores = list(CROSS_ENC_MODEL.predict(a))
#     df["score"] = cross_scores
#     df = df.sort_values('score', ascending=False)
#     return df


# # Loading csv files
# ASPECTS_DF = pd.read_csv(FEATURES_CSV)

# for category in CATEGORY:


#     LIST_OF_PIDS = list(df_pid[df_pid["category_slug"] == category]["pid"])
#     aspects = list(ASPECTS_DF[ASPECTS_DF["category_slug"]==category]["features"])
#     queries = list(ASPECTS_DF[ASPECTS_DF["category_slug"]==category]["query"])
#     aspect_to_query = {aspect:str(query)  for aspect, query in zip(aspects,queries)}
    
#     print("Querying for category : " + str(category))
#     print("These all products will be queried", LIST_OF_PIDS)
    
#     if not os.path.exists(DUMPING_FOLDER + "/" + category):
#         # If it doesn't exist, create the directory
#         os.makedirs(DUMPING_FOLDER + "/" + category)
#         print(f"Directory '{DUMPING_FOLDER} + '/' + {category}' created.")
#     else:
#         print(f"Directory '{DUMPING_FOLDER} + '/' + {category}' already exists.")

#     for pid in LIST_OF_PIDS:
#         combined_data_frame = pd.DataFrame()
#         # For different naming of features
#         for aspect,query in aspect_to_query.items():
#             try:   
#                 response = (
#                     CLIENT.query
#                     .get(WEAVIATE_CLASS_NAME, THINGS_TO_ACCESS)
#                     .with_near_vector({
#                         "vector": MODEL.encode(query),
#                         # "certainty": 0.7
#                     })
#                     .with_additional(["distance"])
#                     .with_limit(LIMIT_FOR_QUERY_RESPONSE)
#                     .with_where({
#                         "path": ["pid"],
#                         "operator": "Equal",
#                         "valueText":"cf9429c4-8cba-11ed-a7ba-930ee103a0a2"
#                     })
#                     .do()
#                 )
#                 # Using only the ones with minimum character length of character_limit_for_review and at max of limit_for_reranking_model
#                 cur_length = 0
#                 print(response)
#                 # Loading our data into dataFrame
#                 df = pd.DataFrame(response['data']["Get"][WEAVIATE_CLASS_NAME])
#             except:
#                     continue

#             if df.empty:
#                 print("No data found for pid " + pid + " for query " + query)
#                 continue
            
#             # Reanking the scores before dumping and pick up only up to size of limit_for_final_output
#             reranked_df = rerank_results(query, df.head(LIMIT_FOR_RERANKING_MODEL))

#             # Pick only some top values after reranking
#             reranked_df = reranked_df.head(LIMIT_FOR_FINAL_OUTPUT)

#             # Counting frequency of a row for which review length repeats and appending that frequency to our dataframe
#             column_to_count = "reviewText"

#             reranked_df['frequency'] = reranked_df.groupby(column_to_count)[column_to_count].transform('count')
#             reranked_df['pid'] = pid
#             reranked_df['aspect'] = aspect
#             reranked_df['query'] = query

#             # Picking the text which will go to OpenAi

#             reranked_df['openAiText'] = reranked_df.apply(lambda row: row['chunkedData'] if row['frequency'] == 1 else row['reviewText'], axis=1)

#             value_counts = reranked_df['openAiText'].value_counts()

#             # Dropping mulptile instances
#             #reranked_df = reranked_df[reranked_df.duplicated(subset='openAiText', keep='first') | ~reranked_df['openAiText'].duplicated(keep=False)]
#             reranked_df = reranked_df[~reranked_df.duplicated(subset=['openAiText'], keep='first')]


#             #combined_data_frame = combined_data_frame.append(reranked_df, ignore_index=True)
#             combined_data_frame = pd.concat([combined_data_frame, reranked_df], ignore_index=True)


#         xlsx_file = DUMPING_FOLDER + "/" + category + "/" + pid + ".xlsx"

#         if not combined_data_frame.empty:
#             combined_data_frame.to_excel(xlsx_file, index=False)