import pandas as pd
import numpy as np
# import spacy
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

INPUT_FILE_PATH = "Output_groupedBy_column.csv"
SIMILARITY_THRESHOLD = 0.9
BATCH_SIZE = 5

df= pd.read_csv(INPUT_FILE_PATH)
df.fillna(0,inplace=True)
df['score'] = 0.0
df['flag']=0

# def find_similarity(openAI_answers, mistral_answers):
#     # nlp = spacy.load('en_core_web_md')
#     # text1 = nlp(text1)
#     # text2 = nlp(text2)
#     # # return text1.similarity(text2)
#     # # if text1.similarity(text2) > SIMILARITY_THRESHOLD:
#     # #     return 1
#     # # return 0
#     # similarity_score = text1.similarity(text2)
#     model = SentenceTransformer('thenlper/gte-large')


#     # sentences=[text1,text2]
#     # model = SentenceTransformer('thenlper/gte-large')
#     # embeddings = model.encode(sentences)
#     # similarity_score=cos_sim(embeddings[0], embeddings[1]).item()
#     # result = [similarity_score, 1 if similarity_score > SIMILARITY_THRESHOLD else 0]
#     # return result

def find_similarity(openAI_answers, mistral_answers):
    model = SentenceTransformer('thenlper/gte-large')
    score_list = []

    i = 0
    while i < len(openAI_answers):
        openAI_sentences = []
        mistral_sentences = []
        openAI_embeddings = []
        mistral_embeddings = []
        indexes = []

        for j in range(i, min(i + BATCH_SIZE, len(openAI_answers))):
            indexes.append(openAI_answers[j]['index'])
            # print(openAI_answers[j]['index']," ")
            openAI_sentences.append(openAI_answers[j]['snippet'])
            mistral_sentences.append(mistral_answers[j]['snippet'])
        openAI_embeddings.extend(model.encode(openAI_sentences))
        mistral_embeddings.extend(model.encode(mistral_sentences))

        for k in range(len(indexes)):
            score = cos_sim(openAI_embeddings[k], mistral_embeddings[k]).item()
            flag = 1 if score > SIMILARITY_THRESHOLD else 0
            index = indexes[k]

            score_list.append({'index': index, 'score': score, 'flag': flag})

        i = i + BATCH_SIZE

    return score_list


# print(df)
mistral_snippets = []
openAI_snippets = []

for index,row in df.iterrows():
    mistral_snippet = row['mistral_output']
    openAI_snippet = row['openAI_output']
    if(mistral_snippet != 0):
        # print(openAI_snippet,"\n",mistral_snippet)

        mistral_snippets.append({'index':index,'snippet':mistral_snippet})
        openAI_snippets.append({'index':index, 'snippet':openAI_snippet})
        # print("OpenAI_snippe: \n", openAI_snippet)
        # print("mistral_snippet: \n", mistral_snippet)
        # print(index, " ")

        # score = find_similarity(mistral_snippet,openAI_snippet)
        # df.loc[index,'score'] = score[0]
        # df.loc[index,'flag'] = score[1]

        # print("ok")
score_list = find_similarity(openAI_snippets, mistral_snippets)

print("\n", score_list)
for scores in score_list:
    index = scores['index']
    score = scores['score']
    flag = scores['flag']
    df.loc[index, 'score'] = score
    df.loc[index, 'flag'] = flag

df.to_csv('similarity_score_using_gte_large.csv')