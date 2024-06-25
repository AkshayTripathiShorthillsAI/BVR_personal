
# import pandas as pd
# from difflib import SequenceMatcher

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

# def process_data(golden_set_path, llama_result_file_path, output_file_path):
#     df_golden = pd.read_excel(golden_set_path)
#     df_llama = pd.read_excel(llama_result_file_path)
    
#     golden_snippets = df_golden['Rephrased Snippets'].tolist()
#     llama_snippets = df_llama['Rephrased Snippet'].tolist()

#     score_list = []
#     for golden_snippet, llama_snippet in zip(golden_snippets, llama_snippets):
#         score = similar(golden_snippet, llama_snippet)
#         score_list.append(score)
    
#     # Create a DataFrame with the similarity scores
#     scores_df = pd.DataFrame({'Similarity Score': score_list})

#     # Save the DataFrame to an Excel file
#     scores_df.to_excel(output_file_path, index=False)

#     return scores_df

# if __name__ == "__main__":
#     golden_set_path = '/home/ankur/projects/llm_test/Akshay/model_check/Face moisturizers.xlsx'
#     llama_result_file_path = '/home/ankur/projects/llm_test/Akshay/model_check/output.xlsx'
#     output_file_path = '/home/ankur/projects/llm_test/Akshay/model_check/similarity_scores.xlsx'
#     scores_df = process_data(golden_set_path, llama_result_file_path, output_file_path)
#     print("Similarity scores saved to:", output_file_path)

import pandas as pd
import spacy

def process_data(golden_set_path, llama_result_file_path, output_file_path):
    # Load English tokenizer, tagger, parser, NER, and word vectors
    nlp = spacy.load("en_core_web_md")

    # Read dataframes
    df_golden = pd.read_excel(golden_set_path)
    df_llama = pd.read_excel(llama_result_file_path)

    # Get snippets as list
    golden_snippets = df_golden['Rephrased Snippets'].tolist()
    llama_snippets = df_llama['Rephrased Snippet'].tolist()

    # Calculate similarity scores
    score_list = []
    for golden_snippet, llama_snippet in zip(golden_snippets, llama_snippets):
        doc_golden = nlp(golden_snippet)
        doc_llama = nlp(llama_snippet)
        score = doc_golden.similarity(doc_llama)
        score_list.append(score)

    # Create a DataFrame with the similarity scores
    scores_df = pd.DataFrame({'Similarity Score': score_list})

    # Save the DataFrame to an Excel file
    scores_df.to_excel(output_file_path, index=False)

    return scores_df

if __name__ == "__main__":
    golden_set_path = '/home/ankur/projects/llm_test/Akshay/model_check/Face moisturizers.xlsx'
    llama_result_file_path = '/home/ankur/projects/llm_test/Akshay/model_check/output.xlsx'
    output_file_path = '/home/ankur/projects/llm_test/Akshay/model_check/similarity_scores.xlsx'
    scores_df = process_data(golden_set_path, llama_result_file_path, output_file_path)
    print("Similarity scores saved to:", output_file_path)
