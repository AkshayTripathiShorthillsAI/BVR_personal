import spacy
import json
import pandas as pd

def find_similarity(text1, text2):
    nlp = spacy.load('en_core_web_md')
    text1 = nlp(text1)
    text2 = nlp(text2)
    if text1.similarity(text2) > float(0.9):
        return True
    return False

def find_score(OPENAI_data, llama3_data):
    aspect_score = find_similarity(OPENAI_data['feature'], llama3_data['feature'])
    snippet_score = find_similarity(OPENAI_data['snippet'], llama3_data['snippet'])
    sentiment_score = find_similarity(OPENAI_data['sentiment'], llama3_data['sentiment'])
    if aspect_score and snippet_score and sentiment_score:
        return 1
    else:
        return 0

def process_data(file_path_excel, file_path_json):
    score_list = []

    with open(file_path_json, 'r') as json_file:
        llama3_data = json.load(json_file)

    df = pd.read_excel(file_path_excel, usecols=['valid_json'])
    first_100_rows_excel = df['valid_json'][:100]
    
    OpenAI_data = []
    for row in first_100_rows_excel:
        try:
            json_object = json.loads(row)
            OpenAI_data.append(json_object)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in row: {row}, Error: {e}")

    for OPENAI_answer, llama3_answer in zip(OpenAI_data, llama3_data):
        final_score = find_score(OPENAI_answer, llama3_answer)
        score_list.append(final_score)

    return score_list

if __name__ == "__main__":

    excel_file_path = 'main_merge_category_snippet_review.xlsx'
    json_file_path = 'llm_answer.json'
    scores = process_data(excel_file_path, json_file_path)
    print(scores)