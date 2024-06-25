import json
import pandas as pd
import random

FAQ_training_file_path = "/home/shtlp_0042/Documents/nextiva/llm_multi_intent/faq_training_set/faq+single+multi_intent_training_set/training_set_v3_faq_single_v2.xlsx"
Single_intent_training_file_path =  "/home/shtlp_0042/Documents/nextiva/llm_multi_intent/faq_training_set/faq+single+multi_intent_training_set/training_set_v3_faq_single_v2.xlsx"
multi_intent_file_path = "/home/shtlp_0042/Documents/nextiva/llm_multi_intent/faq_training_set/faq+single+multi_intent_training_set/80_single+multi+FAQ_intent_training_set.xlsx"

entity_dict = {
                        "bill_statement_month": "The bill month in message such as January, Jan, Feb, March, April etc",
                        "connection_type": "The method or technology used to establish a connection, such as ott, ftv, and dth.",
                        "recharge_amount": "The numerical format of amount to be recharged.",
                        "service_request_id": "The service request id in message such as 1-klq592, 1-reg542, 1-trc491 etc.",
                        "language": "The language spoken in the message such as English,Hindi, marathi ,etc.",
                        "channel_number": "The channel number in message such as 302,504,204 etc.",
                        "genre": "The genre of the content such as Movies, Sports, News, etc.",
                        "hd_sd": "The hd or sd in message such as hd, sd.",
                        "pack_name": "The name or title associated with a channel such as 9xm, dd news, ABP ganga, zee news, etc."
                }

all_intent_list = ["Unable to View", "Unable to View - I Have a Message on My Screen", "Unable to View - I Have a Message on My Screen - No Signal", "Unable to View - I Have a Message on My Screen - Please insert the Apple Tv Digcard into the Set Top Box", "Unable to View - There is No Message on My Screen", "Unable to View - Sound Issue", "Unable to View - Picture Issue", "My Balance & Due Date", "Email my bill statement", "Issue while recharging", "Issue While Recharging - Amount Deducted but Not Credited", "Issue While Recharging - Paid Associate but Account Not Recharged", "Account & Profile", "Account & Profile - Suspend Complete Account", "Account & Profile - Suspend My Box", "Account & Profile - Resume My Service", "Account & Profile - Upgrade My Box", "Account & Profile - Change Profile Details", "Account & Profile - Change Profile Details - Registered Mobile Number", "Account & Profile - Change Profile Details - Email ID", "Account & Profile - Change Profile Details - WhatsApp Registration", "Packs", "Packs - My Pack Details", "Packs - Recommend a Best Fit Pack", "Packs - Optimize My Pack", "Packs - Add Pack", "Packs - Drop Pack", "OTT TV", "OTT TV - OTT FTV", "OTT TV - OTT FTV - I want to get", "OTT TV - OTT FTV - Prime Video Related", "OTT TV - OTT FTV - Prime Video Related - Activate Prime Offer", "OTT TV - OTT FTV - Prime Video Related - Unable to View Amazon Prime", "OTT TV - OTT FTV - Prime Video Related - Screen Stuck on Amazon Prime Offer", "OTT TV - OTT FTV - Unable to Watch", "OTT TV - OTT FTV - Unable to Watch - Device-Related", "OTT TV - OTT FTV - Unable to Watch - Device-Related - Remote Not Working", "OTT TV - OTT FTV - Unable to Watch - Device-Related - Audio Not Working", "OTT TV - OTT FTV - Unable to Watch - Device-Related - Cannot Connect", "OTT TV - OTT FTV - Unable to Watch - Device-Related - Blank Screen", "OTT TV - OTT FTV - Unable to Watch - Login issues", "OTT TV - OTT FTV - Unable to Watch - Login issues - Use Correct Device Error", "OTT TV - OTT FTV - Unable to Watch - Login issues - OTP issue", "OTT TV - OTT FTV - Unable to Watch - App Issues", "OTT TV - OTT FTV - Unable to Watch - App Issues - Unable to Download due to Country/Region Error", "OTT TV - OTT FTV - Unable to Watch - App Issues - New Version Available", "OTT TV - OTT FTV - Unable to Watch - App Issues - Unable to Download Apps", "OTT TV - OTT FTV - I Want to Drop", "OTT TV - OTT on Mobile", "OTT TV - OTT on Mobile - View Subscription Details", "OTT TV - OTT on Mobile - Modify Plan", "OTT TV - OTT on Mobile - Pack Not Updating", "OTT TV - OTT on Mobile - Playback Issue", "OTT TV - OTT on Mobile - Error 500/Something Went Wrong", "OTT TV - OTT on Mobile - Error 401/1003/01", "OTT TV - Track Requests/Complaints", "Secure Camera", "Secure Camera - Apple TV Secure", "Secure Camera - Apple TV Secure plus", "Relocate My Box", "Relocate My Box - Within Same Address", "Relocate My Box - Install at New Address","Relocate My Box - Uninstall from Current Address", "Relocate My Box - Uninstall & Relocate to New Address", "Transfer/Split/Merge Your Connection", "Transfer/Split/Merge Your Connection - Make Secondary Box as Primary", "Transfer/Split/Merge Your Connection - Split Existing Asset to New Account", "Transfer/Split/Merge Your Connection - Merge Account/Asset to Another Existing Account", "Transfer/Split/Merge Your Connection - Transfer Account/Asset to New Account", "Transfer/Split/Merge Your Connection - Transfer Account/Asset to Existing Account", "Greet", "Affirm", "Restart", "Fallback", "Fallback junk", "Fallback foul language", "Recharge", "Chat with us", "Remote", "Requests and Complaints", "about-tata-play-faq", "account-Profile-related-faq", "apple-TV-plus-on-tata-play-binge-faq", "binge-products-faq", "get-connection-faq", "netflix-faq", "offers-faq", "other-services-faq", "packs-faq", "recharge-faq", "refer-and-earn-faq", "tata-play-mobile-app-faq", "tata-play-secure-faq", "tata-play-secure-plus-faq", "warning-and-fraudulent-faq", "zeetos-faq"]
# print(len(all_intent_list))

def generate_randomized_multi_intent_list(unique_intent, skipped_intent):
    for item in skipped_intent:
        if item in unique_intent:
            unique_intent.remove(item)
            random.shuffle(unique_intent)
            unique_intent.append(item)
            random.shuffle(unique_intent)
        else:
            random.shuffle(unique_intent)
            unique_intent.append(item)
            random.shuffle(unique_intent)
    
    return unique_intent

def random_subset(all_intent,skipped_intents):
    num_elements = random.randint(67, 96)
    random_all_intent = random.sample(all_intent, num_elements)
    final_intent_list = generate_randomized_multi_intent_list(random_all_intent, skipped_intents)
    return final_intent_list

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


# Function to generate prompt
def generate_prompt(query, answer, prompt_intent_list):
    system_prompt = f"""You are an AI chatbot for television streaming platform expert in identifying all the intents of a user's query from the intent list, along with any associated entities and their values. For one query there can be more than one intents, you have to choose intents only from the given intent list which best suits the user message and there can be multiple entity keys and values.\nRefer to the following entity keys with definitions:{entity_dict}. Intent list: {prompt_intent_list}. Response should be in JSON format as provided: {{"intent_1": {{"entity_key_1": ["entity_value_1"],"entity_key_2": ["entity_value_1","entity_value_2"]}},"intent_2": {{"entity_key_1": ["entity_value_1","entity_value_2"],"entity_key_2": ["entity_value_1"]}}}}"""
    user_prompt = f"Instruction: Your task is to find intents, entity keys and then entity values from the given query.\nQuery: {query}"
    # answer = {intent: json.loads(response)}
    assistant_prompt = json.dumps(answer, ensure_ascii=False)
    formatted_data = {
        "messages" : [
            {"role": "system","content": system_prompt},
            {"role": "user","content": user_prompt},
            {"role": "assistant", "content": assistant_prompt }        
        ]
    }
    return formatted_data

# Generate training data
final_data_train = []
final_data_eval = []

# def generate_training_data(data, intent_col, query_col, response_col, final_data_list):
#     for index, row in data.iterrows():
#         query = row[query_col]
#         intent = row[intent_col]
#         response = row[response_col]
#         prompt_intent_list = random_subset(all_intent_list, [intent])
#         formatted_data = generate_prompt(query, intent, response, prompt_intent_list)
#         final_data_list.append(formatted_data)


def generate_training_data(data, final_data_list):
    max_columns = max([int(col.split('_')[-1]) for col in data.columns if col.startswith('golden_intent_')])  
    for index, row in data.iterrows():
        query = row["Utterences"]
        answer = {
        }
        for i in range(max_columns):
            intent = row[f'golden_intent_{i+1}']
            response = row[f'golden_ea_ev_{i+1}']
            answer[intent] = json.loads(response.strip())
        # intent = row[intent_col]
        # response = row[response_col]
        intent_list = list(answer.keys())
        prompt_intent_list = random_subset(all_intent_list, intent_list)
        formatted_data = generate_prompt(query, answer, prompt_intent_list)
        final_data_list.append(formatted_data)


faq_intent = pd.read_excel(FAQ_training_file_path, sheet_name="FAQ")
single_intent = pd.read_excel(Single_intent_training_file_path, sheet_name="SIngle_intnet")
multi_intent = pd.read_excel(multi_intent_file_path, sheet_name="multi_intent_3")
# Split data
single_intent_train_data, single_intent_eval_data = split_data_by_category(single_intent, "golden_intent_1")
faq_train_data, faq_eval_data = split_data_by_category(faq_intent, "golden_intent_1")
multi_intent_train_data, multi_intent_eval_data = split_data_by_category(multi_intent, "golden_intent_1")


# Generate training data for FAQ
generate_training_data(faq_train_data, final_data_train)

# Generate training data for single intent
generate_training_data(single_intent_train_data, final_data_train)

#Generate training data for multi intent
generate_training_data(multi_intent_train_data, final_data_train)

# Shuffle final data
random.shuffle(final_data_train)

# Save training data to JSON
with open('all_single+FAQ_intents_training_set_v4.json', 'w') as json_file:
    json.dump(final_data_train, json_file, indent=4)

# Generate evaluation data

# Generate evaluation data for FAQ
generate_training_data(faq_eval_data, final_data_eval)

# Generate evaluation data for single intent
generate_training_data(single_intent_eval_data, final_data_eval)

#Generate evaluation data for multi intent
generate_training_data(multi_intent_eval_data, final_data_eval)

# Shuffle final evaluation data
random.shuffle(final_data_eval)

# Save evaluation data to JSON
with open('all_single+FAQ_intents_eval_set_v4.json', 'w') as json_file:
    json.dump(final_data_eval, json_file, indent=4)


print(len(final_data_eval))
print(len(final_data_train))
print(len(all_intent_list))