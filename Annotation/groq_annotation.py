# # Import statements
# import os
# from dotenv import load_dotenv
# import pandas as pd
# import gc
# import glob
# import groq as Groq


# class QAProcessor:
#     def __init__(self, input_csv):
#         self.input_csv = input_csv
#         self.df = pd.read_csv(input_csv)
#         print(self.df)
#         load_dotenv()

#     def accept_choice(self, aspect, processed_qa_content): 
#         client = Groq(
#             api_key=os.getenv("GROQ_API_KEY"),
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                     {
#                 "role": "system",
#                 "content": '''Your task is to annotate the "processed_qa_content" based on the following instructions:
#                 Instruction:
#                     1. You strcictly have to return one word only YES, NO, OTHER.
#                     2. If processed_qa_content is not related to the given aspect but useful(experienced rich), you will return OTHER.
#                     3. If processed_qa_content is not very general and specifically reflects the experience of user from using the product and is related to the given aspect, then return YES.
#                     4. If processed_qa_content is talking about the product but not reflecting specific user experience, then return NO.'''
#             },
#             {
#                 "role": "user",
#                 "content": '''aspect: smoothness of application of wooden colored pencils
#                     processed_qa_content:The wood bits do not sit evenly across all edges of the pointed end, resulting in awkwardly shaped pencil tips and uneven thickness in doodling.'''
#             },
#             {
#                 "role": "assistant",
#                 "content": f'''YES'''
#             },            
#             {
#                 "role": "user",
#                 "content": '''aspect:comfort grip of wooden colored pencils
#                     processed_qa_content: I always carry these pencils while spending time with younger kids without any fear of them getting messed up or making a mess that can't be easily cleaned up with water.'''
#             },
#             {
#                 "role": "assistant",
#                 "content": f'''OTHER'''
#             },            
#             {
#                 "role": "user",
#                 "content": '''aspect: blendability of wooden colored pencils
#                     processed_qa_content: I found that the color selection allowed me to achieve a full spectrum of colors when blended. The pencils provide smooth, even coverage on a variety of textures and go on with very little pressure, which allowed me to create wonderful gradients. They truly blend when mixed on paper, giving composite hues, in contrast to so many colored pencils that simply smudge together to give a mix of two separate colors.'''
#             },
#             {
#                 "role": "assistant",
#                 "content": f'''NO'''
#             },
#             {
#                 "role": "user",
#                 "content": '''aspect: lead hardness of wooden colored pencils
#                     processed_qa_content: Some of the leads are warped or off center, which makes them break off easily or difficult to get sharp like regular colored pencils.'''
#             },
#             {
#                 "role": "assistant",
#                 "content": f'''YES'''
#             },
#             {
#                 "role": "user",
#                 "content": f'''aspect:{aspect} of bento-boxes
#                     processed_qa_content: {processed_qa_content}'''
#             },
#                 ],
#             model="llama3-70b-8192",
#         )

#         # print(chat_completion.choices[0].message.content)
#         outputs= chat_completion.choices[0].message.content
#         print("Outputs  :" ,outputs)

#         print("FINAL RESPONSE: ", outputs)

#         return outputs

#     def process_and_store(self):
#         # # Process each row and store the result in a new column
#         # print(self.df['aspect'], self.df['Processed_QA_Content'])
#         # self.df['Model_choice'] = self.df.apply(
#         #     lambda row: self.accept_choice(row['aspect'], row['Processed_QA_Content']), axis=1
#         # )
#         # # Save the updated dataframe back to the CSV file
#         # self.df.to_csv(self.input_csv, index=False)
#         print(self.accept_choice("application frequency","When I don't use the enzyme, the water develops a smell faster and eats more chlorine. But with this enzyme, the water feels softer and never gets a scum line or smells."))

# def process_directory(directory_path):
#     # Recursively find all CSV files in the directory
#     csv_files = glob.glob(os.path.join(directory_path, '**/output_final/*.csv'), recursive=True)
#     print(csv_files)
#     processor = QAProcessor("/home/shtlp_0170/Desktop/BVR/Annotation/check_snippet/swimming_pool/final_output/project-781-at-2024-07-03-10-42-362ec32a.csv")
#     processor.process_and_store()
    
#     # for csv_file in csv_files:
#     #     print(f"Processing file: {csv_file}")
#     #     processor = QAProcessor(csv_file)
#     #     processor.accept_choice()

# if __name__ == "__main__":
#     root_directory = "/home/shtlp_0170/Desktop/BVR/Annotation/check_snippet"  
#     process_directory(root_directory)



# ______________________________________________________________________________________________________________________________________________________

# # Import statements
# import os
# from dotenv import load_dotenv
# import pandas as pd
# import glob
# import groq as Groq

# class QAProcessor:
#     def __init__(self, input_csv):
#         self.input_csv = input_csv
#         self.df = pd.read_csv(input_csv)
#         load_dotenv()

#     def accept_choice(self, aspect, processed_qa_content): 
#         client = Groq(
#             api_key=os.getenv("GROQ_API_KEY"),
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": '''Your task is to annotate the "processed_qa_content" based on the following instructions:
#                     Instruction:
#                         1. You strictly have to return one word only: YES, NO, OTHER.
#                         2. If processed_qa_content is not related to the given aspect but useful, you will return OTHER.
#                         3. If processed_qa_content specifically reflects the experience of the user from using the product and is related to the given aspect, then return YES.
#                         4. If processed_qa_content is talking about the product but not reflecting specific user experience, then return NO.'''
#                 },
#                 {
#                     "role": "user",
#                     "content": f'''aspect: {aspect}
#                     processed_qa_content: {processed_qa_content}'''
#                 }
#             ],
#             model="llama3-70b-8192",
#         )

#         outputs = chat_completion.choices[0].message.content.strip()
#         return outputs

#     def process_and_store(self):
#         # Process each row and store the result in a new column
#         self.df['Model_choice'] = self.df.apply(
#             lambda row: self.accept_choice(row['aspect'], row['Processed_QA_Content']), axis=1
#         )
#         # Save the updated dataframe back to the CSV file
#         self.df.to_csv(self.input_csv, index=False)

# def process_directory(directory_path):
#     # Recursively find all CSV files in the directory
#     csv_files = glob.glob(os.path.join(directory_path, '**/output_final/*.csv'), recursive=True)
#     for csv_file in csv_files:
#         print(f"Processing file: {csv_file}")
#         processor = QAProcessor(csv_file)
#         processor.process_and_store()

# if __name__ == "__main__":
#     root_directory = "/home/shtlp_0170/Desktop/BVR/Annotation/check_snippet"
#     process_directory(root_directory)


# ___________________________________________________________________________________________________________________________________________________

# # Import statementsimport os
# from dotenv import load_dotenv
# import groq
# import os

# class QAProcessor:
#     def __init__(self):
#         load_dotenv()

#     def accept_choice(self, aspect, processed_qa_content):
#         # Initialize the client directly
#         client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

#         # Assuming 'chat' and 'completions' are correct attributes to access based on documentation or inspection
        # chat_completion = client.chat.completions.create(
        #     messages=[
        #             {
        #         "role": "system",
        #         "content": '''Your task is to annotate the "processed_qa_content" based on the following instructions:
        #         Instruction:
        #             1. You strcictly have to return one word only YES, NO, OTHER.
        #             2. If processed_qa_content is not related to the given aspect but useful(experienced rich), you will return OTHER.
        #             3. If processed_qa_content is not very general and specifically reflects the experience of user from using the product and is related to the given aspect, then return YES.
        #             4. If processed_qa_content is talking about the product but not reflecting specific user experience, then return NO.'''
        #     },
        #     {
        #         "role": "user",
        #         "content": '''aspect: smoothness of application of wooden colored pencils
        #             processed_qa_content:The wood bits do not sit evenly across all edges of the pointed end, resulting in awkwardly shaped pencil tips and uneven thickness in doodling.'''
        #     },
        #     {
        #         "role": "assistant",
        #         "content": f'''YES'''
        #     },            
        #     {
        #         "role": "user",
        #         "content": '''aspect:comfort grip of wooden colored pencils
        #             processed_qa_content: I always carry these pencils while spending time with younger kids without any fear of them getting messed up or making a mess that can't be easily cleaned up with water.'''
        #     },
        #     {
        #         "role": "assistant",
        #         "content": f'''OTHER'''
        #     },            
        #     {
        #         "role": "user",
        #         "content": '''aspect: blendability of wooden colored pencils
        #             processed_qa_content: I found that the color selection allowed me to achieve a full spectrum of colors when blended. The pencils provide smooth, even coverage on a variety of textures and go on with very little pressure, which allowed me to create wonderful gradients. They truly blend when mixed on paper, giving composite hues, in contrast to so many colored pencils that simply smudge together to give a mix of two separate colors.'''
        #     },
        #     {
        #         "role": "assistant",
        #         "content": f'''NO'''
        #     },
        #     {
        #         "role": "user",
        #         "content": '''aspect: lead hardness of wooden colored pencils
        #             processed_qa_content: Some of the leads are warped or off center, which makes them break off easily or difficult to get sharp like regular colored pencils.'''
        #     },
        #     {
        #         "role": "assistant",
        #         "content": f'''YES'''
        #     },
        #     {
        #         "role": "user",
        #         "content": f'''aspect:{aspect} of bento-boxes
        #             processed_qa_content: {processed_qa_content}'''
        #     },
        #         ],
        #     model="llama3-8b-8192",
        # )


#         outputs = chat_completion.choices[0].message.content.strip()
#         return outputs

# if __name__ == "__main__":
#     # Create an instance of QAProcessor
#     processor = QAProcessor()
    
#     # Test the accept_choice function
#     test_aspect = "application frequency"
#     test_content = "When I don't use the enzyme, the water develops a smell faster and eats more chlorine. But with this enzyme, the water feels softer and never gets a scum line or smells."

#     result = processor.accept_choice(test_aspect, test_content)
#     print("Test Result:", result)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------



#      # Assuming 'chat' and 'completions' are correct attributes to access based on documentation or inspection
        # chat_completion = client.chat.completions.create(
        #     messages=[
        #             {
        #         "role": "system",
        #         "content": '''Your task is to annotate the "processed_qa_content" based on the following instructions:
        #         Instruction:
        #             1. You strcictly have to return one word only YES, NO, OTHER.
        #             2. If processed_qa_content is not related to the given aspect but useful(experienced rich), you will return OTHER.
        #             3. If processed_qa_content is not very general and specifically reflects the experience of user from using the product and is related to the given aspect, then return YES.
        #             4. If processed_qa_content is talking about the product but not reflecting specific user experience, then return NO.
        #     Examples:
        #     aspect: smoothness of application of wooden colored pencils
        #     processed_qa_content:The wood bits do not sit evenly across all edges of the pointed end, resulting in awkwardly shaped pencil tips and uneven thickness in doodling.
        #     Response: YES
            
        #     aspect:comfort grip of wooden colored pencils
        #     processed_qa_content: I always carry these pencils while spending time with younger kids without any fear of them getting messed up or making a mess that can't be easily cleaned up with water.
        #     Response: OTHER
            
        #     aspect: blendability of wooden colored pencils
        #     processed_qa_content: I found that the color selection allowed me to achieve a full spectrum of colors when blended. The pencils provide smooth, even coverage on a variety of textures and go on with very little pressure, which allowed me to create wonderful gradients. They truly blend when mixed on paper, giving composite hues, in contrast to so many colored pencils that simply smudge together to give a mix of two separate colors.
        #     Response: NO
            
        #     aspect: lead hardness of wooden colored pencils
        #     processed_qa_content: Some of the leads are warped or off center, which makes them break off easily or difficult to get sharp like regular colored pencils.
        #     Response: YES
        #     '''
        #     },
        #     {
        #         "role": "user",
        #         "content": f'''aspect:{aspect} of bento-boxes
        #             processed_qa_content: {processed_qa_content}'''
        #     },
        #         ],
        #     model="llama3-8b-8192",
        # )

# ====================================================================================================================================================


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
