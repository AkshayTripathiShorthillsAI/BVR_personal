import pandas as pd
import boto3, json, os
from dotenv import load_dotenv
load_dotenv()

PRODUCT_FILE_FOLDER = os.getenv("PRODUCT_FILE_PATH")     # Downloaded raw files folder
CATEGORY_PRODUCT_DB = "category_all_products.json"
BUCKET_NAME = "bestview-reviews-raw-datas"


class DownloadFileFromS3:
    def __init__(self):
        self.s3_ob = boto3.client("s3")

    def __GetS3(self):
        return self.s3_ob

    def Read_File_From_S3(self, read_path, bucket_name):
        try:
            if not read_path or not bucket_name:
                return "None or Empty Value Not Allowed"
            return (
                self.__GetS3()
                .get_object(Bucket=bucket_name, Key=read_path)["Body"]
                .read()
                .decode("utf-8")
            )
        except Exception as e:
            print("##############")
            print(read_path,bucket_name)
            print("##############")
            raise Exception(str(e))

S3_OBJ = DownloadFileFromS3()

file_path = os.getenv("FILE_PATH_CSV")   # PID CSV FILE PATH
print(file_path)
df = pd.read_csv(file_path)

categories = list(set(list(df["category_slug"].values)))
print(categories)

for category in categories:
    print("$$$$$$$")
    output_path = PRODUCT_FILE_FOLDER +"/" + category
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    product_paths = df[df["category_slug"] == category]["json_file"].values
    print(len(product_paths))
    print("Product Paths",product_paths)
    for path in product_paths:
        try:
            path = path.replace("output_json/", "")
            print("$$$$$$$")
            data = S3_OBJ.Read_File_From_S3(path,BUCKET_NAME)
            with open(f"{output_path}/{path.split('/')[-1]}", 'w', encoding='utf-8') as json_file:
                json.dump(json.loads(data), json_file, ensure_ascii=False, indent=4)
        finally:
            continue