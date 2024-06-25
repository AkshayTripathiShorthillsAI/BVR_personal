from huggingface_hub import login
 
access_token_write = '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'
login(token = access_token_write)
from huggingface_hub import HfApi
api = HfApi()
 
api.upload_folder(
    folder_path="/home/ankur/projects/llm_test/Akshay/fine_tuning/llama3-8b_bvr_v3",
    repo_id="Akshay47/Llama-3-8B-Instruct_bvr_finetune_v3",
    repo_type="model",
)