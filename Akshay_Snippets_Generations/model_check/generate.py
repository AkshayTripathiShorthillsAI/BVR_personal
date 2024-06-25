# Import statements
import os
import glob
import time
import ast
from dotenv import load_dotenv
import pandas as pd
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, AutoConfig
import gc
from vllm import LLM, SamplingParams

import ast
import re

class ReviewSnippets:
    def __init__(self):
        self.df_pid = None
        self.features_df = None
        self.llm = None
        self.sampling_params = None
        self.tokenizer=None
        # load_dotenv("/home/ankur/projects/snippets_all_data/.env")
        load_dotenv()


    def load_configuration(self):
        torch.backends.cuda.enable_mem_efficient_sdp(False)
        torch.backends.cuda.enable_flash_sdp(False)
    
    def load_dataframes(self):
        file_path_csv = os.getenv("FILE_PATH_CSV")
        print("FILE_PATH_CSV value:", file_path_csv)
        if file_path_csv is None:
            print("ERROR: FILE_PATH_CSV is not defined in the .env file.")
            return
        try:
            self.df_pid = pd.read_csv(file_path_csv)
            self.features_df = pd.read_csv(os.getenv("FEATURES_CSV"))
            print(self.features_df)
        except Exception as e:
            print("Error loading CSV file:", e)


    def load_model(self):
        
        # model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        model_name = "/home/ankur/projects/llm_test/Akshay/fine_tuning/llama3-8b_bvr_v2"
        hf_auth = os.getenv("HF_AUTH")
        # model_path = "/home/ankur/.cache/huggingface/hub/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/e5e23bbe8e749ef0efcf16cad411a7d23bd23298"
        model_path= "/home/ankur/projects/llm_test/Akshay/fine_tuning/llama3-8b_bvr_v2"
        # gpu_memory_utilization = float(input("Enter GPU memory utilization (0.0 to 1.0): "))
        self.llm = LLM(model=model_path,
            gpu_memory_utilization= 0.9, #gpu_memory_utilization, 
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

    # Function to be used in old case when we are revieving full text
    def get_snippet_full_review(self, review_text, category_features, category_name):

        messages = [
            {
                "role": "system",
                "content": '''Act as a review classifier. Your task is to extract sentences from the given review text and classify it as experience-rich text based on given classification rules.
 
                Task: You will be provided a review text. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
                    1. Develop a thought: The thought should be clarifying what you need to do next.
                    2. Decide an action: Based on the thought that you have developed, you will decide an action.
                    3. Observation: State your observation, which includes what you have observed after taking the above-decided action.
                    4. Final answer: Give your final answer here and keep the keys in **Final Answer** exactly the same as given in the example.
        
                Classification rules:
                    1. The sentence you extract from the review should be in accordance with the given specifications. You will not select any sentence that is not related to the given list of specs.
                    2. The sentence should reflect the user experience. This means sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review.
                    3. You will return None when there is no specific user experience mentioned in the review text by the user
                    4. You will also return None when you can't find any specification to map for the sentence from the user review text 

                Final Answer example:
                {'feature': 'Consistency ( is the consistency too liquidy or creamy is it easy to apply or gets messy) of face-moisturizers','actual_sentence_extracted': 'This is a non-scented, creamy formula but not oily at all.','rephrased_it(without experience & observation)': 'The user mentioned that the formula is creamy and not oily.','sentiment': 'positive'}
                '''
            },
            {
                "role": "user", 
                "content":f'''Instruction: Extract the experience-rich sentence based on given specification list:
                    Specifications list: {category_features} of {category_name}
                    Review text: {review_text}''' 
            }
        ]
        
        prompt = self.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True
        )
 
        outputs = self.llm.generate(prompt, self.sampling_params)
        print("Outputs  :" ,outputs)
        generated_text = (((outputs[0]).outputs)[0]).text
        torch.cuda.empty_cache()
        gc.collect()

        print("FINAL RESPONSE: ", outputs)
 
        return [generated_text, 0]

    def save_snippets(self):
        # Read the input Excel file
        input_file_path = '/home/ankur/projects/llm_test/Akshay/model_check/Face moisturizers.xlsx'
        df = pd.read_excel(input_file_path)

        # Assuming your input Excel has columns: 'Review text', 'aspect', 'category'
        # and you need to apply the function to each row
        rephrased_snippets = []

        for index, row in df.iterrows():
            each_review_text = row['Review text']
            category_features = row['aspect']
            category = "Face moisturizers"

            try:
                # Call the function and store the result
                output = self.get_snippet_full_review(each_review_text, category_features, category)
                rephrased_snippets.append(output[0])  # Append the generated snippet to the list
            except Exception as e:
                print(f"Error in rephrasing snippet at index {index}: {e}")
                rephrased_snippets.append("")  # Append an empty string if an exception occurs

        # Add the results to a new column in the dataframe
        df['Rephrased Snippet'] = rephrased_snippets

        # Write the updated dataframe to a new Excel file
        output_file_path = '/home/ankur/projects/llm_test/Akshay/model_check/output.xlsx'
        df.to_excel(output_file_path, index=False)

        print(f"Rephrased snippets have been saved to {output_file_path}")



if __name__ == "__main__":
    extractor = ReviewSnippets()
    extractor.load_configuration()
    extractor.load_model()
    extractor.save_snippets()