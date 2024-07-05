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
                "content": '''Your task is to respond with a single word: YES, NO, or OTHER for the provided "processed_qa_content" based on these refined criteria:

Instruction:

YES: Return YES if the content:
It should not be very general
Clearly describes a specific user experience with the product related to the given aspect.
Provides details about usage, performance, or personal observations.
Includes distinctive features or consequences of using the product that are not general but tied to personal experience.
Should not be very general.
Example: "The user mentioned that the markers are smudge proof and bright enough to show up on the black surface, which means they don't rub off on their hands."
NO: Return NO if the content:

Discusses the product in general terms without reflecting a specific user experience.
Lacks personal context or examples and reads more like a product description or advertisement.
Example: "The user mentioned that the Sharpie Permanent Markers are versatile and can be used for various purposes such as labeling boxes for moving, creating intricate designs on posters, or simply doodling in the notebook."

OTHER: Return OTHER if the content:

Is not directly related to the given aspect but still offers valuable information based on the user's experience.
Provides anecdotal insights, general observations, or comments that are informative but not directly tied to the specific aspect in question.
Example: "The user mentioned that the ink has lasted for a year so far, except for the colors that have been lost."

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
