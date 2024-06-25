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
        answer = row["Rephrased Snippets"]
        
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
with open('bvr_training_set_v3.json', 'w') as json_file:
    json.dump(final_data_train, json_file, indent=4)

# Generate evaluation data

# Generate evaluation data for FAQ
generate_training_data(eval_data, final_data_eval)

# Shuffle final evaluation data
random.shuffle(final_data_eval)

# Save evaluation data to JSON
with open('bvr_eval_set_v3.json', 'w') as json_file:
    json.dump(final_data_eval, json_file, indent=4)


print(len(final_data_eval))
print(len(final_data_train))