# Import statements
import os
from dotenv import load_dotenv
import pandas as pd
import torch
import torch.backends  # Import torch.backends together
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoConfig
import gc
from vllm import LLM, SamplingParams
import glob


class QAProcessor:
    def __init__(self):
        self.input_csv = None
        self.df = None
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        load_dotenv()

    def load_configuration(self):
        torch.backends.cuda.enable_mem_efficient_sdp(False)
        torch.backends.cuda.enable_flash_sdp(False)

    def load_model(self):
        
        model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        hf_auth = os.getenv("HF_AUTH")
      
        self.llm = LLM(model=model_name,
            gpu_memory_utilization= 0.9, 
            max_model_len=2048,
        )

        self.sampling_params = SamplingParams(
                                temperature=0.7, 
                                 top_p=0.95,
                                 max_tokens=2048,
                                 )
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=hf_auth
        )

        self.tokenizer.eos_token = "<|eot_id|>"


    def accept_choice(self, aspect, processed_qa_content):
        messages=[
                    {
                "role": "system",
                "content": '''Your task is to respond with a single word: YES, NO, or OTHER for the provided "processed_qa_content"(review) based on these refined criteria:

Instruction for Categorizing Reviews:

YES: Label the review as "YES" if the review contains useful plus unique user-experience that expresses either a positive, negative or neutral experience make sure the snippet is always related to the aspect. The review should highlight how the product meets or exceeds the user's needs or expectations in its primary use.

Indicators:

Descriptions of successful use or satisfaction.
Positive adjectives about the product’s core features.
Examples of benefits received from using the product.

NO: Label the review as "NO" if it describes a negative experience related to the product’s functionality, quality, durability, or alignment with descriptions/expectations. This includes issues such as poor performance, defects, or dissatisfaction with the product.

Indicators:

Complaints about quality or functionality.
Descriptions of problems or unmet expectations.
Negative adjectives or frustration expressed by the reviewer.

Other: Label the review as "Other" if it useful but not related to aspect.

Indicators:

Comments about aspects not crucial to product performance.
Neutral or mixed sentiments.
Observations that do not reflect a clear stance on the product’s primary use.
'''
            },
            {
                "role": "user",
                "content": f'''aspect:{aspect} 
                    processed_qa_content: {processed_qa_content}'''
            },
            ]

        
        prompt = self.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
        )
 
        outputs = self.llm.generate(prompt, self.sampling_params)
        # print("Outputs  :" ,outputs)
        generated_text = (((outputs[0]).outputs)[0]).text
        torch.cuda.empty_cache()
        gc.collect()

        # print("FINAL RESPONSE: ", outputs)

        return generated_text

    def process_and_store(self):
        # Process each row and store the result in a new column
        self.df['Model_choice'] = self.df.apply(
            lambda row: self.accept_choice(row['aspect'], row['Processed_QA_Content']), axis=1
        )
        # Save the updated dataframe back to the CSV file
        self.df.to_csv(self.input_csv, index=False)

    def process_directories(self):
        # Recursively find all CSV files in the specified structure
        root_directory = "/home/ankur/projects/llm_test/Akshay/annotation/Snippets_09_July_2024"
        csv_files = glob.glob(os.path.join(root_directory, '**/output_final/new_concatenated_data.csv'), recursive=True)
        
        for csv_file in csv_files:
            try:
                self.input_csv = csv_file
                self.df = pd.read_csv(csv_file)
                print(f"Processing file: {csv_file}")
                self.process_and_store()
                print(f"Processed and saved file: {csv_file}")
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
            finally:
                torch.cuda.empty_cache()
                gc.collect()




if __name__ == "__main__":
    processor = QAProcessor()
    processor.load_configuration()
    processor.load_model()
    processor.process_directories()