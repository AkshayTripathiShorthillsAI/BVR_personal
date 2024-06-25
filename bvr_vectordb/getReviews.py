
# Continue this tomorrow
import weaviate
import json
import csv
import os
import pandas as pd
import json
from collections import defaultdict
from sentence_transformers import SentenceTransformer, CrossEncoder
from dotenv import load_dotenv
load_dotenv()


# Weaviate Authentication
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_AUTH_KEY = os.getenv("WEAVIATE_AUTH_KEY")

WEAVIATE_CLASS_NAME = "Product_Details_FOR_SNIPPETS"
BATCH_SIZE = 50
WORKERS_COUNT = 10


LIMIT_FOR_QUERY_RESPONSE = 200
LIMIT_FOR_RERANKING_MODEL = 30
LIMIT_FOR_FINAL_OUTPUT = 8
FILE_FOR_COLUMN_NAMES = os.getenv("FILE_FOR_COLUMN_NAMES")
MODEL = SentenceTransformer('thenlper/gte-large')
THINGS_TO_ACCESS = pd.read_excel(FILE_FOR_COLUMN_NAMES)["columnNames"].tolist() 
crs_end_model_card = "cross-encoder/ms-marco-MiniLM-L-12-v2"
CROSS_ENC_MODEL = CrossEncoder(crs_end_model_card, device='cpu')


def rerank_results(query, df):
    print("DF: ", df)
    a = [[query,tx] for tx in df["chunkedData"]]
    cross_scores = list(CROSS_ENC_MODEL.predict(a))
    print(cross_scores)
    df["score"] = cross_scores
    df = df.sort_values('score', ascending=False)
    return df


def batch_callback(callback):
    #print(callback)
    pass

def get_client():
    auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_AUTH_KEY)
 
    client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=auth_config
        )
    
    client.batch.configure(batch_size=BATCH_SIZE,callback=batch_callback, num_workers=WORKERS_COUNT)  # Configure batch
    return client

# CLIENT
CLIENT = get_client()


try:   
        response = (
                    CLIENT.query
                    .get(WEAVIATE_CLASS_NAME, THINGS_TO_ACCESS)
                    .with_near_vector({
                        "vector": MODEL.encode("countertop size"),
                        "certainty": 0.885
                    })
                    .with_additional(["distance"])
                    .with_limit(LIMIT_FOR_QUERY_RESPONSE)
                    .with_where({
                        "path": ["pid"],
                        "operator": "Equal",
                        # "valueText":"ba8331f0-424a-11ee-92e6-6d304ea26a0e"
                        # "valueText":"85d7847a-b576-11ee-92e6-6d304ea26a0e"
                        "valueText":"181eb62a-e207-11ee-9c7c-37d09b6bdb57"
                    })
                    .do()
                )
                # Using only the ones with minimum character length of character_limit_for_review and at max of limit_for_reranking_model
        cur_length = 0
        # print(response)
        with open('response.json', 'w') as json_file:
            json.dump(response, json_file, indent=4)
        print(len(response['data']["Get"][WEAVIATE_CLASS_NAME]))
        df = pd.DataFrame(response['data']["Get"][WEAVIATE_CLASS_NAME])
except Exception as e:
      print(e)


reranked_df = rerank_results("countertop size", df.head(LIMIT_FOR_RERANKING_MODEL))

# Pick only some top values after reranking
reranked_df = reranked_df.head(LIMIT_FOR_FINAL_OUTPUT)

print(reranked_df)
        




# # Continue this tomorrow
# import weaviate
# import json
# import csv
# import os
# import pandas as pd
# import json
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
# MODEL = SentenceTransformer('thenlper/gte-large')
# THINGS_TO_ACCESS = pd.read_excel(FILE_FOR_COLUMN_NAMES)["columnNames"].tolist() 
# crs_end_model_card = "cross-encoder/ms-marco-MiniLM-L-12-v2"
# CROSS_ENC_MODEL = CrossEncoder(crs_end_model_card, device='cpu')


# def rerank_results(query, df):
#     print("DF: ", df)
#     a = [[query,tx] for tx in df["chunkedData"]]
#     cross_scores = list(CROSS_ENC_MODEL.predict(a))
#     df["score"] = cross_scores
#     df = df.sort_values('score', ascending=False)
#     return df


# def batch_callback(callback):
#     #print(callback)
#     pass

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


# try:   
#         response = (
#                     CLIENT.query
#                     .get(WEAVIATE_CLASS_NAME, THINGS_TO_ACCESS)
#                     .with_near_vector({
#                         "vector": MODEL.encode("countertop size"),
#                         "certainty": 0.885
#                     })
#                     .with_additional(["distance"])
#                     .with_limit(LIMIT_FOR_QUERY_RESPONSE)
#                     .with_where({
#                         "path": ["pid"],
#                         "operator": "Equal",
#                         # "valueText":"ba8331f0-424a-11ee-92e6-6d304ea26a0e"
#                         # "valueText":"85d7847a-b576-11ee-92e6-6d304ea26a0e"
#                         "valueText":"85d7847a-b576-11ee-92e6-6d304ea26a0e"
#                     })
#                     .do()
#                 )
#                 # Using only the ones with minimum character length of character_limit_for_review and at max of limit_for_reranking_model
#         cur_length = 0
#         # print(response)
#         with open('response.json', 'w') as json_file:
#             json.dump(response, json_file, indent=4)
#         print(len(response['data']["Get"][WEAVIATE_CLASS_NAME]))
#         df = pd.DataFrame(response['data']["Get"][WEAVIATE_CLASS_NAME])
# except Exception as e:
#       print(e)


# reranked_df = rerank_results("countertop size", df.head(LIMIT_FOR_RERANKING_MODEL))

# # Pick only some top values after reranking
# reranked_df = reranked_df.head(LIMIT_FOR_FINAL_OUTPUT)

# print(reranked_df)
        