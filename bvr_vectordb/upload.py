import json, time, os, weaviate, glob, csv
import logging
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import SpacyTextSplitter
import torch
import gc
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('script.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('my_script')

logger.debug('Script Started')

# For chunking of reviews
SPLITTER_CHUNK_SIZE = 500

# # Weaviate Authentication
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_AUTH_KEY = os.getenv("WEAVIATE_AUTH_KEY")


BATCH_SIZE = 200
WORKERS_COUNT = 5

# File containg pids of files to be uploaded
PIDS_FILE = os.getenv("FILE_PATH_CSV")  # PID file Path

EMBEDDING_BATCH_SIZE = 200
WEAVIATE_CLASS_NAME = "Product_Details_FOR_SNIPPETS"


MAX_REVIEWS = 500

MIN_WORDS_COUNT = 50

# File containing details of pid which was not uploaded on weaviate 
csv_file_path = "unsuccessful.csv"


# Model used in vector encoding
model = SentenceTransformer('thenlper/gte-large')

# Our text splitter
text_splitter = SpacyTextSplitter(chunk_size=SPLITTER_CHUNK_SIZE, pipeline="en_core_web_lg")


# Just empty batch_callback function
def batch_callback(callback):
    #print(callback)
    pass

def get_client():
    try:
        auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_AUTH_KEY)
        client = weaviate.Client(
            url=WEAVIATE_URL,
            auth_client_secret=auth_config
        )  
        client.batch.configure(batch_size=BATCH_SIZE,callback=batch_callback, num_workers=WORKERS_COUNT)  # Configure batch    
        return client
    except:
        print("Time out error in weaviate")
        

# Create weaviate class only once
try:
    client = get_client()
except:
    time.sleep(5)
    client = get_client()


class_obj = {
    "class": WEAVIATE_CLASS_NAME,
    "vectorizer": ""  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
}

# client.schema.create_class(class_obj)


# To vectorize and upload function
def upload_to_vector_db(text_chunks,metadata_chunks,pid):
    vec_list =get_embeddings(text_chunks)
    data_objs = metadata_chunks
        
    add_object(data_objs, vec_list,pid)


# Getting embaddings
def get_embeddings(text):
    try_count = 1
    while True:
        try:
            embeds = model.encode(text, batch_size=EMBEDDING_BATCH_SIZE).tolist()
            gc.collect()
            torch.cuda.empty_cache()

            return embeds

        #*************Shamshad*********************#

        # try:
        #     client = openai.OpenAI(
        #                 base_url = "https://api.endpoints.anyscale.com/v1",
        #                 api_key = ""
        #     )
        #     embedding = client.embeddings.create(
        #                     model="thenlper/gte-large",
        #                     input= text,
        #                 )
        #     embeds = embedding.model_dump()[data][0]['embedding']
        #     print(embeds)
        #     gc.collect()
        #     torch.cuda.empty_cache()
        #     return embeds     
        except Exception as e:
            try_count = try_count + 1
            if try_count == 4:
                print(f"Could not create embedding. Error {e}")
                return "Error in Embedding"
            print(f"Connection error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


# Helper function to upload data
def upload_review(pid,asin,review_df,category):
    logger.debug(f'Starting with one PID: {pid}')
    # This additional metadata contains all the required metadata inside one column
    # TO DO
    # Handles cases where data is not present
    
    review_df['metadata'] = review_df.apply(lambda row: {"section_type":"reviews", "reviewerName" : row["reviewerName"], "reviewerUrl": row["reviewerUrl"], "rating": row["rating"],"reviewTitle":row["reviewTitle"], "reviewDate": row["reviewDate"], "reviewText":row["reviewText"], "is_Helpful":row["is_Helpful"], "reviewText":row["reviewText"],"textLength":row["textLength"], "unique_column":"", "pid": pid, "category": category, "asin": asin}, axis=1)

    metadata_list = []
    reviews_list = []

    for index, row in review_df.iterrows():
        review = row["reviewText"]
        metadata = row["metadata"]
        review_chunks = text_splitter.split_text(review)
        meta_chunks = []
        
        for review_chunk in review_chunks:
            meta = metadata.copy()
            meta["chunkedData"] = review_chunk
            meta_chunks.append(meta)
        
        reviews_list.extend(review_chunks)
        metadata_list.extend(meta_chunks)
    try:
        upload_to_vector_db(reviews_list, metadata_list,pid)
        logger.debug(f'Done with one PID: {pid}')
    except:
        print("Upload error in PID ", pid)
        # continue


# Final function to upload data
def add_object(data_objs, vec_list, pid):
    try:
        with client.batch as batch:
            for i, data_obj in enumerate(data_objs):
                batch.add_data_object(
                    data_obj,
                    WEAVIATE_CLASS_NAME,
                    # vector = data_obj["vector"]
                    vector=vec_list[i]
                )
    except Exception as e:
        print("Unable to upload data for PID " + pid)
        print("Exception e : #### " + str(e))

        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([pid])
    

def remove_duplicates(df):
    df["unique_column"] = df["reviewerName"] + df["reviewTitle"]
    df = df.drop_duplicates(subset=['unique_column'])
    return df
    
def read_product_file(file_name):

    file_obj = open(file_name)
    data = json.load(file_obj)
    reviews = data["reviews"]
    required_keys = [
    "reviewerName",
    "reviewerUrl",
    "rating",
    "reviewTitle",
    "reviewDate",
    "reviewText",
    "is_Helpful",
    "textLength",
    "unique_column"
    ]

    for review in reviews:
     # Check if the required keys are missing and add them with empty strings
     for key in required_keys:
        if key not in review:
            review[key] = ""


    df = pd.DataFrame(reviews)
    if df.shape[0]>0:
        df = remove_duplicates(df)
        df['textLength'] = df['reviewText'].str.split().str.len()
        df= df[df["textLength"]>MIN_WORDS_COUNT]
        
    file_obj.close()

    return df

def convert_to_int(df):
    df['is_Helpful'] = df['is_Helpful'].str.replace('found this helpful','')
    df['is_Helpful'] = df['is_Helpful'].str.replace('people','')
    df['is_Helpful'] = df['is_Helpful'].str.replace('person','')
    df['is_Helpful'] = df['is_Helpful'].str.replace('one','1')

    df['is_Helpful'] = pd.to_numeric(df['is_Helpful'], errors='coerce').fillna(0).astype(int)

    df['rating'] = df['rating'].str.replace('out of 5 stars','')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0).astype(int)
    
    df = df.sort_values(by='is_Helpful', ascending=False)
    return df

def sort_and_add_by_ishelpful(final_df, df):
    temp_df = df[df["is_Helpful"]>0]
    condition = df["is_Helpful"]>0
    df = df[~condition]

    final_df = pd.concat([final_df, temp_df], axis=0)
    return df, final_df

def sort_by_len_and_add_by_rating(final_df, df, rest):
    
    positive_count = round(rest/2)
    negative_count = rest - positive_count
    
    df = df.sort_values(by='textLength', ascending=False)
    
    negative_df = df[(df["rating"]==1) | (df["rating"]==2)][:negative_count]
    if negative_count > negative_df.shape[0]:
        negative_df = df[(df["rating"]==1) | (df["rating"]==2) | (df["rating"]==0)][:negative_count]
        rows_to_remove = negative_df.index
        df = df.drop(rows_to_remove)
    
    positive_df = df[(df["rating"]==5) | (df["rating"]==4)][:negative_count]
    if positive_count > positive_df.shape[0]:
        positive_df = df[(df["rating"]==5) | (df["rating"]==4) |  (df["rating"]==3) | (df["rating"]==0)][:negative_count]
        rows_to_remove = positive_df.index
        df = df.drop(rows_to_remove)
    

    # l = final_df.shape[0]
    # r = MAX_REVIEWS - l
    final_df = pd.concat([positive_df, negative_df, final_df])
    return final_df
    

def get_top_N_reviews(file_name):
        listing_id = file_name.split("/")[-1].split(".")[0]
        final_df = pd.DataFrame()
        df = read_product_file(file_name)

                

        if df.shape[0]>0:
            df = convert_to_int(df)

            df, final_df = sort_and_add_by_ishelpful(final_df, df)

            if final_df.shape[0]<MAX_REVIEWS:
                rest = MAX_REVIEWS - final_df.shape[0]
                final_df = sort_by_len_and_add_by_rating(final_df, df, rest)
            else:
                final_df = final_df[:MAX_REVIEWS]
                
            return final_df
        else:
            print("Reviews missing in ",listing_id )
            return 0

### FLOW OF CODE STARTS FROM HERE ###

product_file_path = os.getenv("PRODUCT_FILE_PATH")      # Downloaded raw files folder

files_and_folders = glob.glob(f'{product_file_path}/**/**', recursive=True)
print(files_and_folders)
files = [f for f in files_and_folders if f.endswith('.json')]
# Removing any duplicate if present
files = list(set(files))

pid_csv = pd.read_csv(PIDS_FILE)

# Print the list of files
logger.debug(f'All files named : {files} will be uploaded')

st_big = time.time()


for file in files:
    st = time.time()
    # # For each file or product we have to upload data to weaviate
    # # File Name

    # # Loading data from json file
    file_object = open(file)
    data = json.load(file_object)
    file_object.close()

    # # Now this is using ASIN instead of PID as we are unable to find PID in this case
    # # That will act as kind of PID in our case
    # # For these 2 products we will use this
    asin = data["ASIN"]
    # pid_csv = pd.read_csv(PIDS_FILE)
    # # output_json/insulated-bottles/raw/B07PKKTQQ9.raw.json
    try:
        pid = pid_csv[pid_csv["json_file"].str.split('/').str[-1].str.split('.').str[0] == asin].head(1)["pid"].values[0]
    except:
        logger.debug(f'Unable to find pid for file : {file}')
        continue
    logger.debug(f'Starting with file named : {file}')
    

    # # Category will also be required in our further flow so also upload that
    category = file.split("/")[1]

    # # Creating an dataframe containing reviews for each PID that would be passed on to upload
    # # Define column names
    # column_names = ["reviewerName","reviewerUrl","rating","reviewTitle","reviewDate","reviewText","is_Helpful","unique_column","textLength"]

    # # Create an empty DataFrame with specified column names
    # df = pd.DataFrame(columns=column_names)
    


    df  = get_top_N_reviews(file)

    #logger.debug("Total reviews that would be injested : ", len(df))
   
    #print("Total reviews that would be injested ", len(df))

    # for d in data["reviews"]:
    #     new_row = { "reviewerName": d["reviewerName"],
    #                 "reviewerUrl": d["reviewerUrl"],
    #                 "rating": d["rating"],
    #                 "reviewTitle": d["reviewTitle"],
    #                 "reviewDate": d["reviewDate"],
    #                 "reviewText": d["reviewText"],
    #                 "is_Helpful": d["is_Helpful"],
    #                 "textLength": len(d["reviewText"]),
    #                 "unique_column": ""
    #             }
    #     # Append the new row to the DataFrame
    #     df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

    if type(df) == pd.DataFrame:
        # l = df.shape[0]
        # print("Asin :", asin, "      Reviews Ingested: ", l)  
        logger.debug(f'Total reviews that would be injested: {len(df)}')      
        upload_review(pid,asin,df,category)
    else:
        print("Reviews missing in ", asin)
        #logger.debug("Review missing in : ", asin)
        logger.debug(f'Review missing in: {asin}')
        
    tt = time.time() - st
    #logger.debug("Time taken for these many reviews (in sec): ", str(tt))
    logger.debug(f'Time takes for these many reviews (in sec): {tt}')


tt_big = time.time() - st_big

logger.debug(f'Total time taken for all uploads (in sec): {tt_big}')


# import json, time, os, weaviate, glob, csv
# import logging
# import openai
# import pandas as pd
# from sentence_transformers import SentenceTransformer
# from langchain.text_splitter import SpacyTextSplitter
# import torch
# import gc
# from dotenv import load_dotenv
# load_dotenv()

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('script.log'),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger('my_script')

# logger.debug('Script Started')

# # For chunking of reviews
# SPLITTER_CHUNK_SIZE = 500

# # # Weaviate Authentication
# WEAVIATE_URL = os.getenv("WEAVIATE_URL")
# WEAVIATE_AUTH_KEY = os.getenv("WEAVIATE_AUTH_KEY")


# BATCH_SIZE = 200
# WORKERS_COUNT = 5

# # File containg pids of files to be uploaded
# PIDS_FILE = os.getenv("FILE_PATH_CSV")  # PID file Path

# EMBEDDING_BATCH_SIZE = 200
# WEAVIATE_CLASS_NAME = "Product_Details_FOR_SNIPPETS"


# MAX_REVIEWS = 500

# MIN_WORDS_COUNT = 50

# # File containing details of pid which was not uploaded on weaviate 
# csv_file_path = "unsuccessful.csv"


# # Model used in vector encoding
# model = SentenceTransformer('thenlper/gte-large')

# # Our text splitter
# text_splitter = SpacyTextSplitter(chunk_size=SPLITTER_CHUNK_SIZE, pipeline="en_core_web_lg")


# # Just empty batch_callback function
# def batch_callback(callback):
#     #print(callback)
#     pass

# def get_client():
#     try:
#         auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_AUTH_KEY)
#         client = weaviate.Client(
#             url=WEAVIATE_URL,
#             auth_client_secret=auth_config
#         )  
#         client.batch.configure(batch_size=BATCH_SIZE,callback=batch_callback, num_workers=WORKERS_COUNT)  # Configure batch    
#         return client
#     except:
#         print("Time out error in weaviate")
        

# # Create weaviate class only once
# try:
#     client = get_client()
# except:
#     time.sleep(5)
#     client = get_client()


# class_obj = {
#     "class": WEAVIATE_CLASS_NAME,
#     "vectorizer": ""  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
# }

# # client.schema.create_class(class_obj)


# # To vectorize and upload function
# def upload_to_vector_db(text_chunks,metadata_chunks,pid):
#     vec_list =get_embeddings(text_chunks)
#     data_objs = metadata_chunks
        
#     add_object(data_objs, vec_list,pid)


# # Getting embaddings
# def get_embeddings(text):
#     try_count = 1
#     while True:
#         try:
#             embeds = model.encode(text, batch_size=EMBEDDING_BATCH_SIZE).tolist()
#             gc.collect()
#             torch.cuda.empty_cache()

#             return embeds

#         #*************Shamshad*********************#

#         # try:
#         #     client = openai.OpenAI(
#         #                 base_url = "https://api.endpoints.anyscale.com/v1",
#         #                 api_key = ""
#         #     )
#         #     embedding = client.embeddings.create(
#         #                     model="thenlper/gte-large",
#         #                     input= text,
#         #                 )
#         #     embeds = embedding.model_dump()[data][0]['embedding']
#         #     print(embeds)
#         #     gc.collect()
#         #     torch.cuda.empty_cache()
#         #     return embeds     
#         except Exception as e:
#             try_count = try_count + 1
#             if try_count == 4:
#                 print(f"Could not create embedding. Error {e}")
#                 return "Error in Embedding"
#             print(f"Connection error: {e}")
#             print("Retrying in 5 seconds...")
#             time.sleep(5)


# # Helper function to upload data
# def upload_review(pid,asin,review_df,category):
#     logger.debug(f'Starting with one PID: {pid}')
#     # This additional metadata contains all the required metadata inside one column
#     # TO DO
#     # Handles cases where data is not present
    
#     review_df['metadata'] = review_df.apply(lambda row: {"section_type":"reviews", "reviewerName" : row["reviewerName"], "reviewerUrl": row["reviewerUrl"], "rating": row["rating"],"reviewTitle":row["reviewTitle"], "reviewDate": row["reviewDate"], "reviewText":row["reviewText"], "is_Helpful":row["is_Helpful"], "reviewText":row["reviewText"],"textLength":row["textLength"], "unique_column":"", "pid": pid, "category": category, "asin": asin}, axis=1)

#     metadata_list = []
#     reviews_list = []

#     for index, row in review_df.iterrows():
#         review = row["reviewText"]
#         metadata = row["metadata"]
#         review_chunks = text_splitter.split_text(review)
#         meta_chunks = []
        
#         for review_chunk in review_chunks:
#             meta = metadata.copy()
#             meta["chunkedData"] = review_chunk
#             meta_chunks.append(meta)
        
#         reviews_list.extend(review_chunks)
#         metadata_list.extend(meta_chunks)
#     try:
#         upload_to_vector_db(reviews_list, metadata_list,pid)
#         logger.debug(f'Done with one PID: {pid}')
#     except:
#         print("Upload error in PID ", pid)
#         # continue


# # Final function to upload data
# def add_object(data_objs, vec_list, pid):
#     try:
#         with client.batch as batch:
#             for i, data_obj in enumerate(data_objs):
#                 batch.add_data_object(
#                     data_obj,
#                     WEAVIATE_CLASS_NAME,
#                     # vector = data_obj["vector"]
#                     vector=vec_list[i]
#                 )
#     except Exception as e:
#         print("Unable to upload data for PID " + pid)
#         print("Exception e : #### " + str(e))

#         with open(csv_file_path, mode="a", newline="") as file:
#             writer = csv.writer(file)
#             writer.writerow([pid])
    

# def remove_duplicates(df):
#     df["unique_column"] = df["reviewerName"] + df["reviewTitle"]
#     df = df.drop_duplicates(subset=['unique_column'])
#     return df
    
# def read_product_file(file_name):

#     file_obj = open(file_name)
#     data = json.load(file_obj)
#     reviews = data["reviews"]
#     required_keys = [
#     "reviewerName",
#     "reviewerUrl",
#     "rating",
#     "reviewTitle",
#     "reviewDate",
#     "reviewText",
#     "is_Helpful",
#     "textLength",
#     "unique_column"
#     ]

#     for review in reviews:
#      # Check if the required keys are missing and add them with empty strings
#      for key in required_keys:
#         if key not in review:
#             review[key] = ""


#     df = pd.DataFrame(reviews)
#     if df.shape[0]>0:
#         df = remove_duplicates(df)
#         df['textLength'] = df['reviewText'].str.split().str.len()
#         df= df[df["textLength"]>MIN_WORDS_COUNT]
        
#     file_obj.close()

#     return df

# def convert_to_int(df):
#     df['is_Helpful'] = df['is_Helpful'].str.replace('found this helpful','')
#     df['is_Helpful'] = df['is_Helpful'].str.replace('people','')
#     df['is_Helpful'] = df['is_Helpful'].str.replace('person','')
#     df['is_Helpful'] = df['is_Helpful'].str.replace('one','1')

#     df['is_Helpful'] = pd.to_numeric(df['is_Helpful'], errors='coerce').fillna(0).astype(int)

#     df['rating'] = df['rating'].str.replace('out of 5 stars','')
#     df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0).astype(int)
    
#     df = df.sort_values(by='is_Helpful', ascending=False)
#     return df

# def sort_and_add_by_ishelpful(final_df, df):
#     temp_df = df[df["is_Helpful"]>0]
#     condition = df["is_Helpful"]>0
#     df = df[~condition]

#     final_df = pd.concat([final_df, temp_df], axis=0)
#     return df, final_df

# def sort_by_len_and_add_by_rating(final_df, df, rest):
    
#     positive_count = round(rest/2)
#     negative_count = rest - positive_count
    
#     df = df.sort_values(by='textLength', ascending=False)
    
#     negative_df = df[(df["rating"]==1) | (df["rating"]==2)][:negative_count]
#     if negative_count > negative_df.shape[0]:
#         negative_df = df[(df["rating"]==1) | (df["rating"]==2) | (df["rating"]==0)][:negative_count]
#         rows_to_remove = negative_df.index
#         df = df.drop(rows_to_remove)
    
#     positive_df = df[(df["rating"]==5) | (df["rating"]==4)][:negative_count]
#     if positive_count > positive_df.shape[0]:
#         positive_df = df[(df["rating"]==5) | (df["rating"]==4) |  (df["rating"]==3) | (df["rating"]==0)][:negative_count]
#         rows_to_remove = positive_df.index
#         df = df.drop(rows_to_remove)
    

#     # l = final_df.shape[0]
#     # r = MAX_REVIEWS - l
#     final_df = pd.concat([positive_df, negative_df, final_df])
#     return final_df
    

# def get_top_N_reviews(file_name):
#         listing_id = file_name.split("/")[-1].split(".")[0]
#         final_df = pd.DataFrame()
#         df = read_product_file(file_name)

                

#         if df.shape[0]>0:
#             df = convert_to_int(df)

#             df, final_df = sort_and_add_by_ishelpful(final_df, df)

#             if final_df.shape[0]<MAX_REVIEWS:
#                 rest = MAX_REVIEWS - final_df.shape[0]
#                 final_df = sort_by_len_and_add_by_rating(final_df, df, rest)
#             else:
#                 final_df = final_df[:MAX_REVIEWS]
                
#             return final_df
#         else:
#             print("Reviews missing in ",listing_id )
#             return 0

# ### FLOW OF CODE STARTS FROM HERE ###

# product_file_path = os.getenv("PRODUCT_FILE_PATH")      # Downloaded raw files folder

# files_and_folders = glob.glob(f'{product_file_path}/**/**', recursive=True)
# print(files_and_folders)
# files = [f for f in files_and_folders if f.endswith('.json')]
# # Removing any duplicate if present
# files = list(set(files))

# pid_csv = pd.read_csv(PIDS_FILE)

# # Print the list of files
# logger.debug(f'All files named : {files} will be uploaded')

# st_big = time.time()


# for file in files:
#     st = time.time()
#     # # For each file or product we have to upload data to weaviate
#     # # File Name

#     # # Loading data from json file
#     file_object = open(file)
#     data = json.load(file_object)
#     file_object.close()

#     # # Now this is using ASIN instead of PID as we are unable to find PID in this case
#     # # That will act as kind of PID in our case
#     # # For these 2 products we will use this
#     asin = data["ASIN"]
#     # pid_csv = pd.read_csv(PIDS_FILE)
#     # # output_json/insulated-bottles/raw/B07PKKTQQ9.raw.json
#     try:
#         pid = pid_csv[pid_csv["json_file"].str.split('/').str[-1].str.split('.').str[0] == asin].head(1)["pid"].values[0]
#     except:
#         logger.debug(f'Unable to find pid for file : {file}')
#         continue
#     logger.debug(f'Starting with file named : {file}')
    

#     # # Category will also be required in our further flow so also upload that
#     category = file.split("/")[1]

#     # # Creating an dataframe containing reviews for each PID that would be passed on to upload
#     # # Define column names
#     # column_names = ["reviewerName","reviewerUrl","rating","reviewTitle","reviewDate","reviewText","is_Helpful","unique_column","textLength"]

#     # # Create an empty DataFrame with specified column names
#     # df = pd.DataFrame(columns=column_names)
    


#     df  = get_top_N_reviews(file)

#     #logger.debug("Total reviews that would be injested : ", len(df))
   
#     #print("Total reviews that would be injested ", len(df))

#     # for d in data["reviews"]:
#     #     new_row = { "reviewerName": d["reviewerName"],
#     #                 "reviewerUrl": d["reviewerUrl"],
#     #                 "rating": d["rating"],
#     #                 "reviewTitle": d["reviewTitle"],
#     #                 "reviewDate": d["reviewDate"],
#     #                 "reviewText": d["reviewText"],
#     #                 "is_Helpful": d["is_Helpful"],
#     #                 "textLength": len(d["reviewText"]),
#     #                 "unique_column": ""
#     #             }
#     #     # Append the new row to the DataFrame
#     #     df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

#     if type(df) == pd.DataFrame:
#         # l = df.shape[0]
#         # print("Asin :", asin, "      Reviews Ingested: ", l)  
#         logger.debug(f'Total reviews that would be injested: {len(df)}')      
#         upload_review(pid,asin,df,category)
#     else:
#         print("Reviews missing in ", asin)
#         #logger.debug("Review missing in : ", asin)
#         logger.debug(f'Review missing in: {asin}')
        
#     tt = time.time() - st
#     #logger.debug("Time taken for these many reviews (in sec): ", str(tt))
#     logger.debug(f'Time takes for these many reviews (in sec): {tt}')


# tt_big = time.time() - st_big

# logger.debug(f'Total time taken for all uploads (in sec): {tt_big}')