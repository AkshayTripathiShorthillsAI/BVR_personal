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
        load_dotenv("/home/ankur/projects/snippets_all_data/.env")
        # load_dotenv()


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
        model_name = "/home/ankur/projects/llm_test/Akshay/fine_tuning/llama3-8b_bvr_v3"
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
                    4. Final answer: Give your final answer here.
        
                Classification rules:
                    1. The sentence you extract from the review should be in accordance with the given specifications. You will not select any sentence that is not related to the given list of specs.
                    2. The sentence should reflect the user experience. This means sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review.
                    3. You will return None when there is no specific user experience mentioned in the review text by the user
                    4. You will also return None when you can't find any specification to map for the sentence from the user review text '''
            },{
                "role": "user", 
                "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
                 Specifications list: [Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder] of Shredders
                 Review text: I am a huge fan of this shredder. It is super quiet compared to other shredders I have used in the past, and shreds the papers into teeny tiny pieces which is great for preventing identity theft. Safety features are great, if your finger is even remotely near the opening it will stop. Highly recommend!''' 
            },
            {
                "role": "assistant", 
                "content": '''{"feature":"Noise level", "actual_sentence_extracted":"It is super quiet compared to other shredders I have used in the past", "rephrased_it(without experience & observation)":"The user mentioned that this shredder is super quiet compared to other shredders he has used in the past", "sentiment":"positive"}, {"feature":"Safety", "actual_sentence_extracted": "Safety features are great, if your finger is even remotely near the opening it will stop", "rephrased_it(without experience & observation)":"The reviewer appreciates the safety features, specifically the mechanism that stops the shredder if a finger or any object is near the opening.", "sentiment":"positive"}''' 
            },
            {
                "role": "user", 
                "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
                    Specifications list: [Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder] of Shredders
                    Review text: This is a great shredder. I’ve never bought one before and needed one. I had a lot of records to shred. I shredded a lot and even got my 80 year old husband to to do it. He can’t do much anymore and this gave him something to do. He figured out how to use and operate the switch without my help., It’s pretty quick and makes a great cut that is not going to allow anyone to put anything back together., I’d recommend this to any home or a small business too.'''
            },  
            {
                "role": "assistant", 
                "content": '''"None"''' 
            }, 
            {
                "role": "user", 
                "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
                    Specifications list: [Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder] of Shredders
                    Review text: You can only shred 2 pages at a time. Anymore, the it takes forever to shred or it jams., Over heats very quickly and when it does takes over an hour to cool off enough to start shredding again., I dont recommend this shredder if you have over 50 pages to shred'''  
            },
            {
                "role": "assistant", 
                "content":  '''{"feature":"Number of sheets of shredder", "actual_sentence_extracted": "You can only shred 2 pages at a time. Anymore, the it takes forever to shred or it jams","rephrased_it(without experience & observation)":"The user has complained that this shredder is limited to shredding only two pages at a time. Attempting to shred more than that results in a slow process or jams.", "sentiment":"negative"}'''  
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


    # Function for new chunked review
    def get_snippet_chunked_review(self, review_text, category_features, category_name): 

        messages = [
    {
        "role": "system",
        "content": '''Act as a review analyser, who can find if the given review is experience-rich based on the exclusive information, the user has mentioned.
        Task: You will be provided a review text. You need to follow the specified flow to classify or nominate the sentence from the review as experience-rich text. Follow the given flow:
        1. Develop a thought: The thought should be clarifying what you need to do next.
        2. Decide an action: Based on the thought that you have developed, you will decide an action.
        3. Observation: State your observation, which includes what you have observed after taking the above-decided action.
        4. Final answer: Give your final answer here and keep the keys in **Final Answer** exactly the same as given in the example.
        
        Classification rules:
        1. The sentence should reflect the user experience. This means sentence refers to that comment of the user in review text that specifically mentions something that has come out because of the personal user experience of that user who has given that review. The sentence should contain the exclusive information that has come out of user experience. 
        2. You will return None when there is no specific user experience mentioned in the review text by the user
        3. You will also return None when you can't find any specification to map for the sentence from the user review text
        4. You should only classify the review as an experience rich sentence only when you find it to have specified information or exclusive information.'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: waterproof (how effectively do the boots keep water out during hikes in wet conditions?) of mens-hiking-boots
        Review text: Honestly surprised by the quality of the boots given the price. The waterproofing works well. I’ve been in the snow and several inches deep in water without ever getting my socks wet. They are super comfortable but a bit warm if not in wearing in colder temps. The fur lining can pull out a bit and stick to your foot if you’re tempted to wear them without socks. Overall a great boot. Wish they lacing system was more solid and the fur properly glued down though.'''
    },
    {
        "role": "assistant",
        "content": '''{"feature": "waterproof of mens-hiking-boots", "actual_sentence_extracted": "I’ve been in the snow and several inches deep in water without ever getting my socks wet.", "rephrased_it(without experience & observation)": "The user mentioned that he has tested the waterproofing of the boots by walking in snow and several inches deep in water and his socks never got wet.","sentiment":"positive"}'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: breathability (how well do the boots allow air circulation to keep feet cool and dry?) of mens-hiking-boots
        Review text: My husband used to wear HI-TEC boots many years ago and had a good experience with the brand. I asked him to try out this pair of HI-TEC Altitude VI I WP Leather Waterproof Mens Hiking Boots which was received in a mens size 12 to see how they fit and compared to his other boots. Overall, he was very impressed with them and really liked how they looked and performed. The only issue he encountered was with how roomy they felt.'''
    },
    {
        "role": "assistant",
        "content": '''"None"'''
    },
    {
        "role": "user",
        "content": '''Instruction: Extract the experience-rich sentence based on given specification: Specification: waterproof (how effectively do the boots keep water out during hikes in wet conditions?) of mens-hiking-boots
        Review text: My husband loves them but after 3 months of moderate wear they leak live sieves. They are about as waterproof as window screen. Keen needs to go back to the drawing board. Overall the fit, weight, comfort are phenomenal. The failed waterproof membrane at 3 months is a show stopper. Had the membranes not failed these would be the most comfortable boots Ive owned in 60 years. Hopefully Keen will fix this issue and they really should extend warranty coverage for what I view is a defective design and or defective materials.'''
    },
    {
        "role": "assistant",
        "content": '''{"feature": "waterproof of mens-hiking-boots", "actual_sentence_extracted": "after 3 months of moderate wear they leak live sieves. They are about as waterproof as window screen", "rephrased_it(without experience & observation)": "The user has complained that the boots are not waterproof and leak after 3 months of moderate wear.", "sentiment": "negative"}'''
    },
    {
        "role": "user",
        "content": f'''Instruction: Extract the experience-rich sentence based on given specification: 
        Specification: {category_features} of {category_name}
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
        print("Generated Text", generated_text )
        torch.cuda.empty_cache()
        gc.collect()

        print("FINAL RESPONSE: ", outputs)
 
        return [generated_text, 0]


    def start_extraction_process(self,reviews, is_helpful, rating, category_features, frequency_list, category, asin_value):
        reviews_list = []
        all_reviews = reviews
        cost_for_all_reviews = []
        rephrased_snippets_for_all_reviews = []
        actual_response_for_all_reviews = []
        time_taken_list = []
        index = 0
        is_helpfuls_list = []
        ratings_list = []
        review_number = []

        for each_review_text, frequency in zip(all_reviews, frequency_list):
            st = time.time()
            output = []

            # Hardcoded
            if frequency == 1:
                output = self.get_snippet_chunked_review(each_review_text, category_features, category)
            else:
                output = self.get_snippet_full_review(each_review_text, category_features, category)

            tt = time.time() - st
            print("Total Time:" , tt)

            actual_response = output[0]
            cost_for_each_review = output[1]
            snips = []
            rephrased_snippets = ""

            if actual_response == "ERROR":
                rephrased_snippets = ""
            else:
                try:
                    rephrased_snippets = output[0]
                    print("Rephrased Snippets" , rephrased_snippets)

                except Exception as e:
                    print("Error in rephrasing snip" + str(e))
                    rephrased_snippets = ""

                # t = rephrased_snippets[:-1]
                t= rephrased_snippets
                t = t.strip()

                try:
                    snips = ast.literal_eval(t)
                    snips = [snips]
                    # snips = str(snips)
                except:
                    rephrased_snippets = t

            if type(snips) == list:
                flag = True
                for snip in snips:
                    reviews_list.append(each_review_text)
                    is_helpfuls_list.append(is_helpful[index])
                    ratings_list.append(rating[index])
                    rephrased_snippets_for_all_reviews.append(snip)
                    actual_response_for_all_reviews.append(actual_response)
                    review_number.append(index + 1)

                    if flag:
                        cost_for_all_reviews.append(cost_for_each_review)
                        time_taken_list.append(tt)
                        flag = False
                    else:
                        cost_for_all_reviews.append("")
                        time_taken_list.append("")
            else:
                reviews_list.append(each_review_text)
                is_helpfuls_list.append(is_helpful[index])
                ratings_list.append(rating[index])

                if snips.lower() == "none":
                    rephrased_snippets = ""

                rephrased_snippets_for_all_reviews.append(rephrased_snippets)
                actual_response_for_all_reviews.append(actual_response)
                cost_for_all_reviews.append(cost_for_each_review)
                time_taken_list.append(tt)
                review_number.append(index + 1)

            # Access the corresponding element in asin_value based on the index
            current_asin_value = asin_value[index]
            index = index + 1
            time.sleep(2)

        final_data = {'Review text': reviews_list,
                    'is_helpful': is_helpfuls_list,
                    'rating': ratings_list,
                    'Actual Response': actual_response_for_all_reviews,
                    'Review Number': review_number,
                    'Rephrased Snippets': rephrased_snippets_for_all_reviews,
                    'Cost per review': cost_for_all_reviews,
                    'Time Taken': time_taken_list,
                    'amazon_page': current_asin_value}

        print(final_data['amazon_page'],final_data['Review text'])

        final_dataframe = pd.DataFrame(final_data)

        return final_dataframe

    # Function to extract rephrased string from Final Answer
    def extract_rephrased(self, data):
        if not isinstance(data, dict):
            return ""
        try:
            # Check for both key variants
            return data.get('rephrased_it(without experience & observation)', "") or data.get('rephrased_it(without experience &amp; observation)', "")
        except Exception as e:
            return ""

    def safe_literal_eval(self, val):
        if isinstance(val, str):
            # Sanitize the input string
            sanitized_val = re.sub(r'[\r\n]', ' ', val)  # Remove newlines
            try:
                return ast.literal_eval(sanitized_val)
            except (ValueError, SyntaxError) as e:
                print(f"Failed to parse {val}: {e}")
                return None
        return val
    
    # Function to save snippets in excel
    def save_snippets(self):
        desired_column_order = ["is_helpful", "rating", "Actual Response", "Review Number", "Cost per review",	"Time Taken", "amazon_page", "Review text", "Rephrased Snippets", "aspect", "QA_Content", "Accept"]
        CATEGORY = self.df_pid['category_slug'].unique()

        for category in CATEGORY:
            
            files_and_folders = glob.glob(f'{os.getenv("DUMPING_FOLDER_FILTERED_FEATURES")}/{category}/**', recursive=True)
            files = [f for f in files_and_folders if f.endswith('.xlsx')]
            print(files)
            category_features = list(self.features_df[self.features_df["category_slug"]==category]["features"])
            print(category_features)
            if category_features == "":
                print(f"Category Features missing for catrgory {category} in csv file")
                exit()
            
            category_snippet_folder= f'{os.getenv("CATEGORY_SNIPPET_FOLDER")}/{category}'   
            if not os.path.exists(category_snippet_folder):
                os.makedirs(category_snippet_folder)
                
            for file in files:
                listing_id = file.split("/")[-1].split(".")[0]
                
                print(file)
                df = pd.read_excel(file)

                combined_data_frame = pd.DataFrame()

                for aspect in category_features:
                    asin_value=df[df["aspect"]==aspect]['asin'].to_list()
                    review_list = df[df["aspect"]==aspect]['openAiText'].to_list()
                    is_helpful = df[df["aspect"]==aspect]['is_Helpful'].to_list()
                    rating = df[df["aspect"]==aspect]["rating"].to_list()
                    frequency = (df[df["aspect"]==aspect]["frequency"]).to_list()
                        
                    if len(review_list)>0:
                        final_dataframe = self.start_extraction_process(review_list, is_helpful,rating, aspect,frequency, category,asin_value)
                        final_dataframe["amazon_page"]=f"https://amazon.com/dp/{asin_value[0]}"
                        # final_dataframe["amazon_page"]="https://amazon.com/dp/B007F9XHAY"
                        final_dataframe["aspect"] = aspect
                        for column in desired_column_order:
                            if column not in final_dataframe.columns:
                                final_dataframe[column] = ''
                        
                        # Sanitize and parse 'Rephrased Snippets' before applying extract_rephrased
                        final_dataframe['Rephrased Snippets'] = final_dataframe['Rephrased Snippets'].apply(self.safe_literal_eval)
                        final_dataframe['QA_Content'] = final_dataframe['Rephrased Snippets'].apply(self.extract_rephrased)
                        final_dataframe = final_dataframe[desired_column_order]
                        combined_data_frame = pd.concat([combined_data_frame, final_dataframe], ignore_index=True)
                        
                combined_data_frame.to_excel(f"{category_snippet_folder}/{listing_id}_snippets.xlsx")


if __name__ == "__main__":
    extractor = ReviewSnippets()
    extractor.load_dataframes()
    extractor.load_configuration()
    extractor.load_model()
    extractor.save_snippets()