import os
from dotenv import load_dotenv
import pandas as pd
import glob
import groq

class QAProcessor:
    def __init__(self, input_csv):
        self.input_csv = input_csv
        self.df = pd.read_csv(input_csv)
        load_dotenv()

    def accept_choice(self, aspect, processed_qa_content):
        client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                    {
                "role": "system",
                "content": '''Your task is to respond with a single word: YES, NO, or OTHER for the provided "processed_qa_content"(review) based on these refined criteria:

Instruction for Categorizing Reviews:

YES: Label the review as "YES" if it is related to aspect and clearly expresses a positive experience regarding the product’s functionality, quality, effectiveness, or comfort. The review should highlight how the product meets or exceeds the user's needs or expectations in its primary use.

Indicators:

Descriptions of successful use or satisfaction.
Positive adjectives about the product’s core features.
Examples of benefits received from using the product.
NO: Label the review as "NO" if it describes a negative experience related to the product’s functionality, quality, durability, or alignment with descriptions/expectations. This includes issues such as poor performance, defects, or dissatisfaction with the product.

Indicators:

Complaints about quality or functionality.
Descriptions of problems or unmet expectations.
Negative adjectives or frustration expressed by the reviewer.
Other: Label the review as "Other" if it provides general comments, neutral observations, or remarks that are not directly related to the product’s main features. This includes feedback on non-essential aspects or general opinions that do not clearly express strong satisfaction or dissatisfaction.

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
                ],
            model="llama3-8b-8192",
        )


        outputs = chat_completion.choices[0].message.content.strip()
        print(outputs)
        return outputs

    def process_and_store(self):
        self.df['Model_choice'] = self.df.apply(
            lambda row: self.accept_choice(row['aspect'], row['Processed_QA_Content']), axis=1
        )
        self.df.to_csv(self.input_csv, index=False)
        print(f"Processed and stored results to {self.input_csv}")

def process_directory(directory_path):
    # Recursively find all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, '**/*.csv'), recursive=True)

    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        processor = QAProcessor(csv_file)
        processor.process_and_store()

if __name__ == "__main__":
    root_directory = "/home/shtlp_0170/Desktop/BVR/Annotation/check_snippet"  
    process_directory(root_directory)
