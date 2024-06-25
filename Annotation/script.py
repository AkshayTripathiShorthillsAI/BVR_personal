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
    def __init__(self, input_csv):
        self.input_csv = input_csv
        self.df = pd.read_csv(input_csv)
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        load_dotenv()

    def load_configuration(self):
        torch.backends.cuda.enable_mem_efficient_sdp(False)
        torch.backends.cuda.enable_flash_sdp(False)

    def load_model(self):
        
        model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
        # model_name = "/home/ankur/projects/llm_test/Akshay/fine_tuning/llama3-8b_bvr_v3"
        hf_auth = os.getenv("HF_AUTH")
      
        # gpu_memory_utilization = float(input("Enter GPU memory utilization (0.0 to 1.0): "))
        self.llm = LLM(model=model_name,
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

    # def accept_choice(self, aspect, processed_qa_content):
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": '''Your task is to annotate the "processed_qa_content" based on the following instructions:
    #             Instruction:
    #                 1. You strcictly have to return one word only YES, NO, OTHER.
    #                 2. If processed_qa_content is not related to the given aspect, you will return OTHER.
    #                 3. If processed_qa_content is very general, talking about the product but not reflecting specific user experience, then return NO.
    #                 4. If processed_qa_content is not very general and specifically reflects the experience of user from using the product and is related to the given aspect, then return YES.'''
    #         },
    #         {
    #             "role": "user",
    #             "content": '''aspect: smoothness of application of wooden colored pencils
    #                 processed_qa_content:The wood bits do not sit evenly across all edges of the pointed end, resulting in awkwardly shaped pencil tips and uneven thickness in doodling.'''
    #         },
    #         {
    #             "role": "assistant",
    #             "content": f'''YES'''
    #         },            
    #         {
    #             "role": "user",
    #             "content": '''aspect:comfort grip of wooden colored pencils
    #                 processed_qa_content: I always carry these pencils while spending time with younger kids without any fear of them getting messed up or making a mess that can't be easily cleaned up with water.'''
    #         },
    #         {
    #             "role": "assistant",
    #             "content": f'''OTHER'''
    #         },            
    #         {
    #             "role": "user",
    #             "content": '''aspect: blendability of wooden colored pencils
    #                 processed_qa_content: I found that the color selection allowed me to achieve a full spectrum of colors when blended. The pencils provide smooth, even coverage on a variety of textures and go on with very little pressure, which allowed me to create wonderful gradients. They truly blend when mixed on paper, giving composite hues, in contrast to so many colored pencils that simply smudge together to give a mix of two separate colors.'''
    #         },
    #         {
    #             "role": "assistant",
    #             "content": f'''NO'''
    #         },
    #         {
    #             "role": "user",
    #             "content": '''aspect: lead hardness of wooden colored pencils
    #                 processed_qa_content: Some of the leads are warped or off center, which makes them break off easily or difficult to get sharp like regular colored pencils.'''
    #         },
    #         {
    #             "role": "assistant",
    #             "content": f'''YES'''
    #         },
    #         {
    #             "role": "user",
    #             "content": f'''aspect:{aspect} of bento-boxes
    #                 processed_qa_content: {processed_qa_content}'''
    #         },
    #     ]

    def accept_choice(self, aspect, processed_qa_content):
        messages = [
            {
                "role": "system",
                "content": '''Your task is to annotate the "processed_qa_content" based on the following instructions:
                Instruction:
                    1. You strcictly have to return one word only YES, NO, OTHER.
                    2. If processed_qa_content is not related to the given aspect but useful(experienced rich), you will return OTHER.
                    3. If processed_qa_content is not very general and specifically reflects the experience of user from using the product and is related to the given aspect, then return YES.
                    4. If processed_qa_content is talking about the product but not reflecting specific user experience, then return NO.'''
            },
            {
                "role": "user",
                "content": '''aspect: smoothness of application of wooden colored pencils
                    processed_qa_content:The wood bits do not sit evenly across all edges of the pointed end, resulting in awkwardly shaped pencil tips and uneven thickness in doodling.'''
            },
            {
                "role": "assistant",
                "content": f'''YES'''
            },            
            {
                "role": "user",
                "content": '''aspect:comfort grip of wooden colored pencils
                    processed_qa_content: I always carry these pencils while spending time with younger kids without any fear of them getting messed up or making a mess that can't be easily cleaned up with water.'''
            },
            {
                "role": "assistant",
                "content": f'''OTHER'''
            },            
            {
                "role": "user",
                "content": '''aspect: blendability of wooden colored pencils
                    processed_qa_content: I found that the color selection allowed me to achieve a full spectrum of colors when blended. The pencils provide smooth, even coverage on a variety of textures and go on with very little pressure, which allowed me to create wonderful gradients. They truly blend when mixed on paper, giving composite hues, in contrast to so many colored pencils that simply smudge together to give a mix of two separate colors.'''
            },
            {
                "role": "assistant",
                "content": f'''NO'''
            },
            {
                "role": "user",
                "content": '''aspect: lead hardness of wooden colored pencils
                    processed_qa_content: Some of the leads are warped or off center, which makes them break off easily or difficult to get sharp like regular colored pencils.'''
            },
            {
                "role": "assistant",
                "content": f'''YES'''
            },
            {
                "role": "user",
                "content": f'''aspect:{aspect} of bento-boxes
                    processed_qa_content: {processed_qa_content}'''
            },
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

        return generated_text

    def process_and_store(self):
        # Process each row and store the result in a new column
        self.df['Model_choice'] = self.df.apply(
            lambda row: self.accept_choice(row['aspect'], row['Processed_QA_Content']), axis=1
        )
        # Save the updated dataframe back to the CSV file
        self.df.to_csv(self.input_csv, index=False)

def process_directory(directory_path):
    # Recursively find all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, '**/output_final/*.csv'), recursive=True)
    print(csv_files)
    
    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        processor = QAProcessor(csv_file)
        processor.load_configuration()
        processor.load_model()
        processor.process_and_store()

if __name__ == "__main__":
    root_directory = "/home/ankur/projects/llm_test/Akshay/snippets/check_snippets_2"  
    process_directory(root_directory)
