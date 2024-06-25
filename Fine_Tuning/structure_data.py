import json
import pandas as pd
import random

training_file_path = "combined_data.csv"

def split_data_by_category(dataframe, category_column):
    # Identify unique categories
    unique_categories = dataframe[category_column].unique()

    # Initialize DataFrame to store 80% of data
    remaining_data = pd.DataFrame()

    # Iterate through unique categories
    for category in unique_categories:
        # Select rows for the current category
        category_data = dataframe[dataframe[category_column] == category]
        num_rows_to_select = int(len(category_data) * 0.2)
        
        # Randomly select 20% of rows
        selected_rows = category_data.sample(n=num_rows_to_select)
        
        # Append selected rows to remaining_data
        remaining_data = pd.concat([remaining_data, selected_rows])
        
    # Get the rest of the data (80%)
    remaining_indices = dataframe.index.difference(remaining_data.index)
    rest_of_the_data = dataframe.iloc[remaining_indices]
    
    return rest_of_the_data, remaining_data

# # 
#             {
#                 "role": "user", 
#                 "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
#                  Specifications list: [Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder] of Shredders
#                  Review text: I am a huge fan of this shredder. It is super quiet compared to other shredders I have used in the past, and shreds the papers into teeny tiny pieces which is great for preventing identity theft. Safety features are great, if your finger is even remotely near the opening it will stop. Highly recommend!''' 
#             },
#             {
#                 "role": "assistant", 
#                 "content": '''{
#                            "Thought" : "I need to extract experience-rich sentence from user review text based on given specification list.",
#                            "Action" : "Find[Finding a text sentence from the review based on specification list]",
#                            "Observation" : "I could extract one sentence based on specification -- Noise level (how noisy it is to operate the shredder). The sentence i extracted is -- 'It is super quiet compared to other shredders I have used in the past'. Sentiment for feature (Noise level) in review is positive",
#                            "Thought" : "I have found one sentence. I need to check if it is experience-rich",
#                            "Action" : "Check experience-rich[Checking if the found sentence is experience-rich or not?]",
#                            "Observation": "The user mentioned that he has come to the conclusion of saying it super quiet after using it and also using other shredders too. Thus, it can be said that user has commeted that based on his experience. So, it is experience-rich sentence.",
#                            "Thought" : "I have found one experience-rich sentence. Total of 1 experience-rich sentence found till now. Before giving final answer, let me check if i can find more such sentences.",
#                            "Action" : "Find[Finding a unique text sentence, a different one, but based on specification list]",
#                            "Observation" : "I could extract another sentence based on specification -- Safety(how safe the shredder is to ease). The sentence i extracted is -- 'Safety features are great, if your finger is even remotely near the opening it will stop'. User seems satisfied with respect to feature (safety) so it shows positive sentiment towards safety",
#                            "Thought" : "I have found another sentence. I need to check if it is experience-rich",
#                            "Action" : "Check experience-rich[Checking if the found sentence is experience-rich or not?]",
#                            "Observation": "The user specifically mentions that even if your finger is remotely near the opening it will stop. From this statement it seems that user has used this shredder himself and then found that how safe it is. Thus, it can be said that user has commeted based on his experience. So, it is experience-rich sentence.",
#                            "Thought" : "I have found another experience-rich sentence. Total of 2 experience-rich sentence found till now. Before giving final answer, let me check if i can find more such sentences.",
#                            "Action" : "Find[Finding a unique text sentence, a different one, but based on specification list]",
#                            "Observation" : "I could not find any other sentence related to given specification list",
#                            "Thought" : "Since, no new sentence found, i should give final answer with the previous 2 experience-rich sentences.",
#                            "Final answer" : [{"feature":"Noise level", "actual_sentence_extracted":"It is super quiet compared to other shredders I have used in the past", "rephrased_it(without experience & observation)":"The user mentioned that this shredder is super quiet compared to other shredders he has used in the past", "sentiment":"positive"}, {"feature":"Safety", "actual_sentence_extracted": "Safety features are great, if your finger is even remotely near the opening it will stop", "rephrased_it(without experience & observation)":"The reviewer appreciates the safety features, specifically the mechanism that stops the shredder if a finger or any object is near the opening.", "sentiment":"positive"}]
#                            }''' 
#             },
#             {
#                 "role": "user", 
#                 "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
#                     Specifications list: [Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder] of Shredders
#                     Review text: This is a great shredder. I’ve never bought one before and needed one. I had a lot of records to shred. I shredded a lot and even got my 80 year old husband to to do it. He can’t do much anymore and this gave him something to do. He figured out how to use and operate the switch without my help., It’s pretty quick and makes a great cut that is not going to allow anyone to put anything back together., I’d recommend this to any home or a small business too.'''
#             },  
#             {
#                 "role": "assistant", 
#                 "content": '''{
#                            "Thought" : "I need to extract experience-rich sentence from user review text based on given specification list.",
#                            "Action" : "Find[Finding a text sentence from the review based on specification list]",
#                            "Observation" : "I could not extract any sentence based on given specifications. Nothing is related to Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder",
#                            "Thought" : "Since there is no sentence found based on specifications, then as per rule 4 of Classification rules, i should return None",
#                            "Final answer" : "None"}''' 
#             }, 
#             {
#                 "role": "user", 
#                 "content": '''Instruction: Extract the experience-rich sentence based on given specification list:
#                     Specifications list: [Safety(how safe the shredder is to ease), Ease of use (how easy it is to clean the shredder), Number of sheets of shredder, Noise level (how noisy it is to operate the shredder), Maneuvering (how easy it is to carry the shredder from one place to another), Versatile (how versatile is shredder is, in terms of handling various materials), Bin size of shredder] of Shredders
#                     Review text: You can only shred 2 pages at a time. Anymore, the it takes forever to shred or it jams., Over heats very quickly and when it does takes over an hour to cool off enough to start shredding again., I dont recommend this shredder if you have over 50 pages to shred'''  
#             },
#             {
#                 "role": "assistant", 
#                 "content":  '''{
#                            "Thought" : "I need to extract experience-rich sentence from user review text based on given specification list.",
#                            "Action" : "Find[Finding a text sentence from the review based on specification list]",
#                            "Observation" : "I could extract one sentence based on specification -- Number of sheets of shredder. The sentence i extracted is -- 'You can only shred 2 pages at a time. Anymore, the it takes forever to shred or it jams",
#                            "Thought" : "I have found one snipet. I need to check if it is experience-rich",
#                            "Action" : "Check experience-rich[Checking if the found sentence is experience-rich or not?]",
#                            "Observation": "The user has complained that it shreds only 2 pages at a time, and right after it, he has also said that attempting to shred more results in a slow process or jams. From this statement, it seems that the user has used the shredder and has faced this problem personally. Thus, it can be said that user has commeted that based on his experience. So, it is experience-rich sentence. This review expresses the negative feedback from customer with respect to feature: Number of sheets of shredder.",
#                            "Thought" : "I have found one experience-rich sentence. Total of 1 experience-rich sentence found till now. Before giving final answer, let me check if i can find more such sentences.",
#                            "Action" : "Find[Finding a unique text sentence, a different one, but based on specification list]",
#                            "Observation" : "I could not find any other sentence related to given specification list",
#                            "Thought" : "Since, no new sentence found, i should give final answer with the previous 1 experience-rich sentences.",
#                            "Final answer" : [{"feature":"Number of sheets of shredder", "actual_sentence_extracted": "You can only shred 2 pages at a time. Anymore, the it takes forever to shred or it jams","rephrased_it(without experience & observation)":"The user has complained that this shredder is limited to shredding only two pages at a time. Attempting to shred more than that results in a slow process or jams.", "sentiment":"negative"}]
#                            }'''  
#             },

# Function to generate prompt
def generate_prompt(review_text, category_features, category_name, answer):
    assistant_prompt = json.dumps(answer, ensure_ascii=False)
    formatted_data = {
       "messages" : [
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
},
{
"role": "user", 
"content":f'''Instruction: Extract the experience-rich sentence based on given specification list:
Specifications list: {category_features} of {category_name}
Review text: {review_text}''' 
},
{"role": "assistant", "content": assistant_prompt }  
]}
    return formatted_data

# Generate training data
final_data_train = []
final_data_eval = []

def generate_training_data(data, final_data_list):
    
    for index, row in data.iterrows():
        review_text = row["Review text"]
        category_features = row["aspect"]
        category_name = row["category_name"]
        answer = row["Actual Response"]
        
        formatted_data = generate_prompt(review_text, category_features, category_name, answer)
        final_data_list.append(formatted_data)


snippets_data = pd.read_csv(training_file_path)

# Split data
train_data, eval_data = split_data_by_category(snippets_data, "category_name")


# Generate training data for FAQ
generate_training_data(train_data, final_data_train)

# Shuffle final data
random.shuffle(final_data_train)

# Save training data to JSON
with open('bvr_training_set_v2.json', 'w') as json_file:
    json.dump(final_data_train, json_file, indent=4)

# Generate evaluation data

# Generate evaluation data for FAQ
generate_training_data(eval_data, final_data_eval)

# Shuffle final evaluation data
random.shuffle(final_data_eval)

# Save evaluation data to JSON
with open('bvr_eval_set_v2.json', 'w') as json_file:
    json.dump(final_data_eval, json_file, indent=4)


print(len(final_data_eval))
print(len(final_data_train))