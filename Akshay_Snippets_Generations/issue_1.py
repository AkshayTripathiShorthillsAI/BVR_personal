# Import statements
import os
from dotenv import load_dotenv
        
load_dotenv("/home/ankur/projects/snippets_all_data/.env")


value = os.getenv("OPENAI_API_TYPE")

print("OPENAI_API_TYPE", value)