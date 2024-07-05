# # Import statements
# import os
# import pandas as pd
# from groq import Groq 
# from dotenv import load_dotenv

# class ReviewSnippets:
#     def __init__(self):
#         self.df_pid = None
#         self.features_df = None
#         load_dotenv()


#     # Function to be used in old case when we are revieving full text
#     def get_aspects(self ,category_name):
#         client = Groq(
#             api_key=os.getenv("GROQ_API_KEY"),
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                     {
#                         "role": "system",
#                         "content": '''generate aspects of a category , i need aspects on which generally user talk about while giving reviews on any product example:
# Category Slug: loose-leaf-binder-paper 
# Aspects: [Paper Quality, Ink Absorption, Hole Strength, Line Spacing, Whiteness, Quantity per Pack, Tear line, Environment friendly, Price Point,Binder compatibility]
# Category Slug: art-paintbrush-sets 
# Aspects: [Brush Variety, Bristle Quality, Grip Comfort, Versatility, Durability, Ease of Cleaning, Appearance, Bristle Stability
# Category Slug: liquid-highlighters
# Aspects: [Color Vibrancy,nk Flow, Drying Time, Smudge Resistance, Tip Durability, Transparency, Ergonomic Design, Ink Longevity, Versatility, Odor

# '''
#                     },
#                     {
#                         "role": "user", 
#                         "content":f'''Category Slug: {category_name}
# Aspects:''' 
#                     }
#                 ],
#             model="llama3-8b-8192",
#         )

#         # print(chat_completion.choices[0].message.content)
#         outputs= chat_completion.choices[0].message.content
#         final_response=outputs

#         print("FINAL RESPONSE: ", outputs)
 
#         return [final_response, 0]

# if __name__ == "__main__":
#     extractor = ReviewSnippets()
#     extractor.get_aspects("hair-brushes")

# # Import statements
# import pandas as pd
# import os
# from groq import Groq
# import re 
# import ast 
# import csv
# import json
# from dotenv import load_dotenv

# class ReviewSnippets:
#     def __init__(self):
#         self.df_pid = None
#         self.features_df = None
#         load_dotenv()


#     # Function to be used in old case when we are revieving full text
#     def get_aspects(self ,category_name):
#         client = Groq(
#             api_key=os.getenv("GROQ_API_KEY"),
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                     {
#                         "role": "system",
#                         "content": '''generate aspects of a category , i need 10 aspects (on which generally user talk about while giving reviews) and corresponding data as per following instructions and generate JSON string as Final Response:

#                         Instructions:
#                         1. Identify Product Categories: Determine the product categories for which you need to create the table. For example, "permanent markers," "lunch boxes," "bed frames," etc.
#                         2. Define Aspects: Determine the specific aspects or characteristics that you want to include in the table for each product category. Aspects could be things like "Ink Longevity," "Durability," "Ease of Cleaning," etc.
#                         3. Create Positive Taglines: Think of positive taglines that describe each aspect in a favorable light. These taglines should highlight the positive attributes of the product category for each aspect. For example, "Long-lasting ink that retains its color for years."
#                         4. Create Mixed Taglines: Develop mixed taglines that acknowledge both positive and negative aspects of each category. These taglines should reflect both the strengths and weaknesses of the product category for each aspect. For example, "{X} Praised for durability, but {Y} users found it cracked easily."
#                         5. Include Synonyms: Provide synonyms for each aspect to enhance understanding and clarity. Synonyms could be alternative terms or phrases that convey the same meaning as the aspect. For example, "Durability" could also be referred to as "Staying Power" or "Longevity."
#                         6. Create the Table: Organize all the information into a structured table format. Include columns for the category slug, aspects, positive taglines, mixed taglines, and synonyms.

# Final Response: [{Category Slug: insulated-tumblers,Aspect:Insulation Performance,Tagline (Positive):Were satisfied with the insulation,Aspect Explanation:How well the tumbler maintains the temperature of beverages. For example, keeping drinks hot or cold for hours.,Tagline (Mixed):{X} were satisfied with the insulation, but {Y} found it lacking.,Synonyms:Temperature Retention, Thermal Efficiency
# }]
# '''
#                     },
#                     {
#                         "role": "user", 
#                         "content":f'''Category Slug: throw-pillows''' 
#                  },{
#                         "role": "assistant", 
#                         "content":'''[
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Comfort",
#         "Tagline (Positive)": "Softness and plushness that provides ultimate comfort while sitting and relaxing",
#         "Aspect Explanation": "How well the pillow supports the head and neck during use, including its softness, shape, and material",
#         "Tagline (Mixed)": "{X} praised the comfort, though {Y} felt it could be softer",
#         "Synonyms": "Cushioning, Softness"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Fabric Quality",
#         "Tagline (Positive)": "Appreciated the fabric quality",
#         "Aspect Explanation": "The quality of the fabric used. For example, being durable, soft, and pleasant to touch.",
#         "Tagline (Mixed)": "{X} appreciated the fabric quality, while {Y} thought it was rough",
#         "Synonyms": "Material, Fabric Durability"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Design",
#         "Tagline (Positive)": "Liked the design",
#         "Aspect Explanation": "The visual appeal and aesthetic design of the pillow. For example, having trendy patterns and colors.",
#         "Tagline (Mixed)": "{X} liked the design, although {Y} found it too plain",
#         "Synonyms": "Aesthetics, Appearance"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Stitching",
#         "Tagline (Positive)": "Praised the stitching",
#         "Aspect Explanation": "The quality and durability of the stitching. For example, ensuring the pillow remains intact over time.",
#         "Tagline (Mixed)": "{X} praised the stitching, but {Y} noticed it unraveling",
#         "Synonyms": "Sewing Quality, Seam Strength"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Shape Retention",
#         "Tagline (Positive)": "Found it retains shape well",
#         "Aspect Explanation": "How well the pillow maintains its shape after use. For example, not becoming flat or misshapen.",
#         "Tagline (Mixed)": "{X} found it retains shape well, though {Y} saw it flattening",
#         "Synonyms": "Resilience, Form Stability"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Versatility",
#         "Tagline (Positive)": "Liked its versatility",
#         "Aspect Explanation": "The ability to use the pillow in various settings. For example, suitable for couches, beds, and chairs.",
#         "Tagline (Mixed)": "{X} liked its versatility, but {Y} found it limited",
#         "Synonyms": "Multi-Purpose, Adaptability"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Colorfastness",
#         "Tagline (Positive)": "Appreciated the colorfastness",
#         "Aspect Explanation": "The resistance of the fabric color to fading or running. For example, maintaining vibrant colors after washing.",
#         "Tagline (Mixed)": "{X} appreciated the colorfastness, while {Y} noticed fading",
#         "Synonyms": "Dye Stability, Color Retention"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Filling Quality",
#         "Tagline (Positive)": "Liked the filling quality",
#         "Aspect Explanation": "The quality of the pillow's filling. For example, using materials that provide good support and comfort.",
#         "Tagline (Mixed)": "{X} liked the filling quality, but {Y} found it lumpy",
#         "Synonyms": "Stuffing, Interior Material"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Hypoallergenic",
#         "Tagline (Positive)": "Praised its hypoallergenic nature",
#         "Aspect Explanation": "The pillow's suitability for people with allergies. For example, using materials that prevent allergic reactions.",
#         "Tagline (Mixed)": "{X} praised its hypoallergenic nature, although {Y} experienced issues",
#         "Synonyms": "Allergy-Friendly, Non-Allergenic"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Ease of Cleaning",
#         "Tagline (Positive)": "Appreciated the ease of cleaning",
#         "Aspect Explanation": "How simple it is to clean the pillow. For example, being machine washable or having a removable cover.",
#         "Tagline (Mixed)": "{X} appreciated the ease of cleaning, while {Y} found it difficult",
#         "Synonyms": "Maintenance, Care"
#     }
# ]''' 
#                  },{
#                         "role": "user", 
#                         "content":f'''Category Slug: {category_name}''' 
#                  },
#                 ],
#             model="llama3-8b-8192",
#         )

#         # print(chat_completion.choices[0].message.content)
#         outputs= chat_completion.choices[0].message.content
#         final_response=str(outputs)

#         print(final_response)
#         # Parse JSON string into a list of dictionaries
#         data = json.loads(final_response)

#         # Define CSV file name
#         csv_file_name = 'output.csv'

#         # Writing data to CSV
#         with open(csv_file_name, mode='w', newline='') as csv_file:
#             writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
#             writer.writeheader()
#             for item in data:
#                 writer.writerow(item)

#         print(f"Data successfully written to {csv_file_name}")

#         # print("FINAL RESPONSE: ", outputs)
 
#         return final_response
    
#     def extract_dictionaries(self, text):
#         # Regex to match dictionaries enclosed in curly braces
#         pattern = re.compile(r'\{.*?\}', re.DOTALL)
        
#         # Find all matches
#         matches = pattern.findall(text)
        
#         # Convert matched strings to dictionaries
#         dictionaries = [ast.literal_eval(match) for match in matches]
        
#         print(dictionaries)
        
#         return dictionaries
    
#     def save_to_csv(self, dictionaries, csv_file):
#         # Check if file exists to decide whether to write headers
#         file_exists = os.path.isfile(csv_file)

#         with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
#             fieldnames = dictionaries[0].keys()  # Assuming all dictionaries have the same keys

#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             # Write headers only if the file is new
#             if not file_exists:
#                 writer.writeheader()

#             # Write each dictionary as a row
#             for cat in dictionaries:
#                 writer.writerow(cat)

# if __name__ == "__main__":
#     extractor = ReviewSnippets()
#     # extractor.get_aspects("centrifugal-juicers")
#     categories = ["throw-pillows", "centrifugal-juicers", "masticating-juicers", "food-chopper", "fat-burners"]
#     for category in categories:
#         final_response = extractor.get_aspects(category)
#         print(type(final_response))
#         print(final_response)
#         for elem in final_response:
#             print(elem)
#             print("____________________________________________________________________________________________________")
#         res2 =  extractor.extract_dictionaries(final_response)
#         for cat in res2:
#             print("_______________________________________________________________________________")
#             print(cat)
     
#         # Define the CSV file path
#         csv_file = f'Asins_data.csv'

#         # Save dictionaries to CSV
#         extractor.save_to_csv(res2, csv_file)

#         print(f'Data successfully saved to {csv_file}')

# if __name__ == "__main__":
#     extractor = ReviewSnippets()
#     categories = ["throw-pillows", "centrifugal-juicers"]
#     for category in categories:
#         print("Processing ", category)
#         aspect_table = extractor.get_aspects(category)
#         print(aspect_table)
#         parsed_data = extractor.parse_response(aspect_table)
#         extractor.save_to_csv(parsed_data, f"{category}_aspects.csv")

# import pandas as pd
# import json
# import os
# from groq import Groq
# from dotenv import load_dotenv

# class ReviewSnippets:
#     def __init__(self):
#         self.df_pid = None
#         self.features_df = None
#         load_dotenv()

#     def get_aspects(self, category_name):
#         client = Groq(
#             api_key=os.getenv('GROQ_API_KEY'),
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": '''generate aspects of a category , i need 10 aspects on which generally user talk about while giving reviews on any product.
#                     JSON Result should be like Final Response (keys should be strictly same)

#                     Instructions:
#                     1. Identify Product Categories: Determine the product categories for which you need to create the table. For example, "permanent markers," "lunch boxes," "bed frames," etc.
#                     2. Define Aspects: Determine the specific aspects or characteristics that you want to include in the table for each product category. Aspects could be things like "Ink Longevity," "Durability," "Ease of Cleaning," etc.
#                     3. Create Positive Taglines: Think of positive taglines that describe each aspect in a favorable light. These taglines should highlight the positive attributes of the product category for each aspect. For example, "Long-lasting ink that retains its color for years."
#                     4. Create Mixed Taglines: Develop mixed taglines that acknowledge both positive and negative aspects of each category. These taglines should reflect both the strengths and weaknesses of the product category for each aspect. For example, "Praised for durability, but some users found it cracked easily."
#                     5. Include Synonyms: Provide synonyms for each aspect to enhance understanding and clarity. Synonyms could be alternative terms or phrases that convey the same meaning as the aspect. For example, "Durability" could also be referred to as "Staying Power" or "Longevity."
#                     6. Create the Table: Organize all the information into a structured table format. Include columns for the category slug, aspects, positive taglines, mixed taglines, and synonyms.

#                     example:
#                     Final Response: {Category Slug: insulated-tumblers,Aspect:Insulation Performance,Tagline (Positive):Were satisfied with the insulation,Aspect Explanation:How well the tumbler maintains the temperature of beverages. For example, keeping drinks hot or cold for hours.,Tagline (Mixed):{X} were satisfied with the insulation, but {Y} found it lacking.,Synonyms:Temperature Retention, Thermal Efficiency
#                     }
#                     '''
#                 },
#                 {
#                     "role": "user",
#                     "content": f'''Category Slug: {category_name}
#                     Final Response:'''
#                 }
#             ],
#             model="llama3-8b-8192",
#         )

#         outputs = chat_completion.choices[0].message.content
#         final_response = outputs
#         print(final_response)

#         return final_response

    # def parse_response(self, response):
    #     aspect_data = {
    #         "Category Slug": [],
    #         "Aspect": [],
    #         "Tagline (Positive)": [],
    #         "Aspect Explanation": [],
    #         "Tagline (Mixed)": [],
    #         "Synonyms": []
    #     }

    #     for category_slug, aspects in response.items():
    #         for aspect in aspects:
    #             aspect_data["Category Slug"].append(category_slug)
    #             aspect_data["Aspect"].append(aspect["aspect"])
    #             aspect_data["Tagline (Positive)"].append(aspect["positive_tagline"])
    #             aspect_data["Aspect Explanation"].append("")  # Assuming no explanation in current data
    #             aspect_data["Tagline (Mixed)"].append(aspect["mixed_tagline"])
    #             aspect_data["Synonyms"].append(", ".join(aspect["synonyms"]))

    #     return pd.DataFrame(aspect_data)

    # def save_to_csv(self, df, filename):
    #     if not df.empty:
    #         df.to_csv(filename, index=False)
    #         print(f"Data saved to {filename}")
    #     else:
    #         print(f"No data to save to {filename}")

# if __name__ == "__main__":
#     extractor = ReviewSnippets()
#     categories = ["throw-pillows", "centrifugal-juicers", "masticating-juicers", "food-chopper", "fat-burners"]
#     for category in categories:
#         print("Processing ", category)
#         aspect_table = extractor.get_aspects(category)
        # print(aspect_table)
        # parsed_data = extractor.parse_response(aspect_table)
        # extractor.save_to_csv(parsed_data, f"{category}_aspects.csv")

# import pandas as pd
# import json
# from groq import Groq

# class ReviewSnippets:
#     def __init__(self):
#         self.df_pid = None
#         self.features_df = None

#     def get_aspects(self, category_name):
#         client = Groq(
#             api_key="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",
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": '''generate aspects of a category , i need 10 aspects on which generally user talk about while giving reviews on any product.
#                     JSON Result should be like Final Response (keys should be strictly same)

#                     Instructions:
#                     1. Identify Product Categories: Determine the product categories for which you need to create the table. For example, "permanent markers," "lunch boxes," "bed frames," etc.
#                     2. Define Aspects: Determine the specific aspects or characteristics that you want to include in the table for each product category. Aspects could be things like "Ink Longevity," "Durability," "Ease of Cleaning," etc.
#                     3. Create Positive Taglines: Think of positive taglines that describe each aspect in a favorable light. These taglines should highlight the positive attributes of the product category for each aspect. For example, "Long-lasting ink that retains its color for years."
#                     4. Create Mixed Taglines: Develop mixed taglines that acknowledge both positive and negative aspects of each category. These taglines should reflect both the strengths and weaknesses of the product category for each aspect. For example, "Praised for durability, but some users found it cracked easily."
#                     5. Include Synonyms: Provide synonyms for each aspect to enhance understanding and clarity. Synonyms could be alternative terms or phrases that convey the same meaning as the aspect. For example, "Durability" could also be referred to as "Staying Power" or "Longevity."
#                     6. Create the Table: Organize all the information into a structured table format. Include columns for the category slug, aspects, positive taglines, mixed taglines, and synonyms.

#                     example:
#                     Final Response: {Category Slug: insulated-tumblers,Aspect:Insulation Performance,Tagline (Positive):Were satisfied with the insulation,Aspect Explanation:How well the tumbler maintains the temperature of beverages. For example, keeping drinks hot or cold for hours.,Tagline (Mixed):{X} were satisfied with the insulation, but {Y} found it lacking.,Synonyms:Temperature Retention, Thermal Efficiency
#                     }
#                     '''
#                 },
#                 {
#                     "role": "user",
#                     "content": f'''Category Slug: {category_name}
#                     Final Response:'''
#                 }
#             ],
#             model="llama3-8b-8192",
#         )

#         outputs = chat_completion.choices[0].message.content.strip()  # Strip any extra whitespace
#         print(f"Raw Output:\n{outputs}\n")  # Debugging: Print the raw output

#         if not outputs:
#             print(f"Error: Received empty response for category '{category_name}'")
#             return None

#         try:
#             final_response = json.loads(outputs)  # Parse the JSON string
#         except json.JSONDecodeError as e:
#             print(f"JSONDecodeError: {e}")
#             return None

#         print(f"Parsed Response:\n{final_response}\n")  # Debugging: Print the parsed JSON

#         aspect_data = {
#             "Category Slug": [],
#             "Aspect": [],
#             "Tagline (Positive)": [],
#             "Aspect Explanation": [],
#             "Tagline (Mixed)": [],
#             "Synonyms": []
#         }

#         # Iterating through the parsed JSON data
#         for aspect in final_response:
#             aspect_data["Category Slug"].append(final_response["Category Slug"])
#             aspect_data["Aspect"].append(aspect["Aspect"])
#             aspect_data["Tagline (Positive)"].append(aspect["Tagline (Positive)"])
#             aspect_data["Aspect Explanation"].append(aspect["Aspect Explanation"])
#             aspect_data["Tagline (Mixed)"].append(aspect["Tagline (Mixed)"])
#             aspect_data["Synonyms"].append(", ".join(aspect["Synonyms"]))

#         df = pd.DataFrame(aspect_data)
#         df.to_csv(f"llama_snippets_{category_name}.csv", index=False)  # Save to CSV with category name
#         print(f"Data saved for category {category_name}")
        
#         return final_response
        

# if __name__ == "__main__":
#     extractor = ReviewSnippets()
#     categories = ["throw-pillows", "centrifugal-juicers", "masticating-juicers", "food-chopper", "fat-burners"]
#     for category in categories:
#         print("Processing ", category)
#         aspect_table = extractor.get_aspects(category)




# # -----------------------------------------------------------------------------------------------------------------------------------------------------
# # ----------------------------------------------------Working Code------------------------------------------------------------------------------------

# import pandas as pd
# import os
# from groq import Groq
# import re 
# from dotenv import load_dotenv
# import csv
# import json

# class ReviewSnippets:
#     def __init__(self):
#         self.df_pid = None
#         self.features_df = None
#         load_dotenv()


#     # Function to be used in old case when we are revieving full text
#     def get_aspects(self ,category_name):
#         client = Groq(
#             api_key=os.getenv("GROQ_API_KEY"),
#         )

#         chat_completion = client.chat.completions.create(
#             messages=[
#                     {
#                         "role": "system",
#                         "content": '''generate JSON string for 10 aspects of category (on which generally user talk about while giving reviews).Follow below Instructions :

#                         Instructions:
#                         1. Identify Product Categories: Determine the product categories for which you need to create the table. For example, "permanent markers," "lunch boxes," "bed frames," etc.
#                         2. Define Aspects: Determine the specific aspects or characteristics that you want to include in the table for each product category. Aspects could be things like "Ink Longevity," "Durability," "Ease of Cleaning," etc. Dont include these Aspects: "Warranty and Support", "Price and Value".
#                         3. Create Positive Taglines: Think of positive taglines that describe each aspect in a favorable light. These taglines should highlight the positive attributes of the product category for each aspect. For example, "Long-lasting ink that retains its color for years."
#                         4. Create Mixed Taglines: Develop mixed taglines that acknowledge both positive and negative aspects of each category. These taglines should reflect both the strengths and weaknesses of the product category for each aspect. For example, "{X} Praised for durability, but {Y} users found it cracked easily."
#                         5. Include Synonyms: Provide synonyms for each aspect to enhance understanding and clarity. Synonyms could be alternative terms or phrases that convey the same meaning as the aspect. For example, "Durability" could also be referred to as "Staying Power" or "Longevity."
#                         6. Create the Table: Organize all the information into a structured table format. Include columns for the category slug, aspects, positive taglines, mixed taglines, and synonyms.

# Final Response: [{"Category Slug": "insulated-tumblers","Aspect":"Insulation Performance","Tagline (Positive)":"Were satisfied with the insulation","Aspect Explanation":"How well the tumbler maintains the temperature of beverages. For example, keeping drinks hot or cold for hours.","Tagline (Mixed)":"{X} were satisfied with the insulation, but {Y} found it lacking.","Synonyms":"Temperature Retention, Thermal Efficiency"
# }]
# '''
#                     },
#                     {
#                         "role": "user", 
#                         "content":f'''Category Slug: throw-pillows''' 
#                  },{
#                         "role": "assistant", 
#                         "content":'''[
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Comfort",
#         "Tagline (Positive)": "Softness and plushness that provides ultimate comfort while sitting and relaxing",
#         "Aspect Explanation": "How well the pillow supports the head and neck during use, including its softness, shape, and material",
#         "Tagline (Mixed)": "{X} praised the comfort, though {Y} felt it could be softer",
#         "Synonyms": "Cushioning, Softness"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Fabric Quality",
#         "Tagline (Positive)": "Appreciated the fabric quality",
#         "Aspect Explanation": "The quality of the fabric used. For example, being durable, soft, and pleasant to touch.",
#         "Tagline (Mixed)": "{X} appreciated the fabric quality, while {Y} thought it was rough",
#         "Synonyms": "Material, Fabric Durability"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Design",
#         "Tagline (Positive)": "Liked the design",
#         "Aspect Explanation": "The visual appeal and aesthetic design of the pillow. For example, having trendy patterns and colors.",
#         "Tagline (Mixed)": "{X} liked the design, although {Y} found it too plain",
#         "Synonyms": "Aesthetics, Appearance"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Stitching",
#         "Tagline (Positive)": "Praised the stitching",
#         "Aspect Explanation": "The quality and durability of the stitching. For example, ensuring the pillow remains intact over time.",
#         "Tagline (Mixed)": "{X} praised the stitching, but {Y} noticed it unraveling",
#         "Synonyms": "Sewing Quality, Seam Strength"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Shape Retention",
#         "Tagline (Positive)": "Found it retains shape well",
#         "Aspect Explanation": "How well the pillow maintains its shape after use. For example, not becoming flat or misshapen.",
#         "Tagline (Mixed)": "{X} found it retains shape well, though {Y} saw it flattening",
#         "Synonyms": "Resilience, Form Stability"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Versatility",
#         "Tagline (Positive)": "Liked its versatility",
#         "Aspect Explanation": "The ability to use the pillow in various settings. For example, suitable for couches, beds, and chairs.",
#         "Tagline (Mixed)": "{X} liked its versatility, but {Y} found it limited",
#         "Synonyms": "Multi-Purpose, Adaptability"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Colorfastness",
#         "Tagline (Positive)": "Appreciated the colorfastness",
#         "Aspect Explanation": "The resistance of the fabric color to fading or running. For example, maintaining vibrant colors after washing.",
#         "Tagline (Mixed)": "{X} appreciated the colorfastness, while {Y} noticed fading",
#         "Synonyms": "Dye Stability, Color Retention"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Filling Quality",
#         "Tagline (Positive)": "Liked the filling quality",
#         "Aspect Explanation": "The quality of the pillow's filling. For example, using materials that provide good support and comfort.",
#         "Tagline (Mixed)": "{X} liked the filling quality, but {Y} found it lumpy",
#         "Synonyms": "Stuffing, Interior Material"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Hypoallergenic",
#         "Tagline (Positive)": "Praised its hypoallergenic nature",
#         "Aspect Explanation": "The pillow's suitability for people with allergies. For example, using materials that prevent allergic reactions.",
#         "Tagline (Mixed)": "{X} praised its hypoallergenic nature, although {Y} experienced issues",
#         "Synonyms": "Allergy-Friendly, Non-Allergenic"
#     },
#     {
#         "Category Slug": "throw-pillows",
#         "Aspect": "Ease of Cleaning",
#         "Tagline (Positive)": "Appreciated the ease of cleaning",
#         "Aspect Explanation": "How simple it is to clean the pillow. For example, being machine washable or having a removable cover.",
#         "Tagline (Mixed)": "{X} appreciated the ease of cleaning, while {Y} found it difficult",
#         "Synonyms": "Maintenance, Care"
#     }
# ]''' 
#                  },{
#                         "role": "user", 
#                         "content":f'''Category Slug: {category_name}''' 
#                  },
#                 ],
#             model="llama3-70b-8192",
#         )

#         # print(chat_completion.choices[0].message.content)
#         outputs= chat_completion.choices[0].message.content
#         final_response=str(outputs)
#         json_string = re.sub(r'^[^\[]*\[', '[', final_response, 1)

#         print(final_response)
#         # Parse JSON string into a list of dictionaries
#         data = json.loads(json_string)

#         # Define CSV file name
#         csv_file_name = 'llama_Aspect.csv'


#         file_exists = os.path.isfile(csv_file_name)

#         # Writing data to CSV
#         with open(csv_file_name, mode='a', newline='') as csv_file:
#             # Get the fieldnames from the first dictionary
#             fieldnames = data[0].keys()
#             writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#             # Write header only if the file does not exist or is empty
#             if not file_exists:
#                 writer.writeheader()

#             # Write rows to the CSV file
#             for item in data:
#                 writer.writerow(item)

#         print(f"Data successfully written to {csv_file_name}")

#         # print("FINAL RESPONSE: ", outputs)
 
#         return final_response

# if __name__ == "__main__":
#     extractor = ReviewSnippets()
#     csv_file_name = 'llama_Aspect.csv'


#     file_exists = os.path.isfile(csv_file_name)

#     headers = [
#     "Category Slug",
#     "Aspect",
#     "Tagline (Positive)",
#     "Aspect Explanation",
#     "Tagline (Mixed)",
#     "Synonyms"
# ]

#     # Writing data to CSV
#     with open(csv_file_name, mode='w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(headers)
    
#     # Get the fieldnames from the first dictionary
#     # extractor.get_aspects("centrifugal-juicers")
#     # categories = ["travel-packing-organizers", "usb-cables", "usb-hubs", "waist-packs", "wall-tabletop-picture-frames", "webcams", "wine-glasses", "wireless-bluetooth-speakers", "womens-athletic-outdoor-sandals-slides", "womens-bikini-sets", "womens-casual-dresses", "womens-down-jackets-parkas", "womens-jumpsuits", "womens-minimizer-bras", "womens-pullover-sweaters"]

#     categories = [" sports-nutrition-nitric-oxide-boosters", "carb-blockers-supplements", "multi-enzyme-nutritional-supplements", "l-glutamine-nutritional-supplements", "power-hedge-trimmers", "full-car-covers", "landscape-path-lights", "turmeric-herbal-supplements", "dog-hip-joint-care", "vehicle-cargo-carriers", "dog-grooming-clippers", "portable-solar-chargers", "womens-boots", "mens-boots", "boomboxes", "training-collars", "joint-muscle-pain-relief-rubs", "cd-players", "car-wax", "mens-rotary-shavers", "walking-canes", "dog-probiotic-supplements", "table-fans", "mens-water-shoes", "camping-chairs","traction-equipment", "car-seat-head-body-supports", "portable-dvd-players", "body-weight-scales-digital", "home-audio-subwoofers", "laptop-bags", "exterior-paint", "fishing-rods", "bassinets", "sporting-optics-mounts", "high-chair", "projection-screens", "hunting-shooting-earmuffs", "kids-tricycles", "coq10-nutritional-supplements", "exterior-care-products", "automotive-bug-sap-tar-removers", "Chrome & Metal Polishes", "Cleaners", "hiking-daypacks", "omega-3-6-9-oil-nutritional-supplements", "space-heaters", "roasted-coffee-beans","standard-baby-strollers", "psyllium-nutritional-supplement"]
#     for category in categories:
#         final_response = extractor.get_aspects(category)




# --------------------------------Changing Prompt-------------------------------------


import pandas as pd
import os
from groq import Groq
import re 
from dotenv import load_dotenv
import csv
import json

class ReviewSnippets:
    def __init__(self):
        self.df_pid = None
        self.features_df = None
        load_dotenv()


    # Function to be used in old case when we are revieving full text
    def get_aspects(self ,category_name):
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                    {
                        "role": "system",
                        "content": '''generate JSON string for 10 aspects of category (on which generally user talk about while giving reviews).Follow below Instructions :

                        Instructions:
                        1. Identify Product Categories: Determine the product categories. For example, "permanent markers", "loose-leaf-binder-paper","bed frames", etc.
                        2. Define Aspects: Determine the specific aspects or characteristics that you want to include for each product category. Aspects could be things like "Ink Longevity," "Paper Quality", "Tear line", etc. Dont include these Aspects: "Warranty and Support", "Price and Value".
                        3. Create Positive Taglines: Think of positive taglines that describe each aspect in a favorable light. These taglines should highlight the positive attributes of the product category for each aspect.For example, "Praised the paper quality","Appreciated the ink absorption","Liked the quantity per pack".It should start with words like:"Appreciated" , "Liked" , "Found" , "Praised" etc
                        4. Create Mixed Taglines: Develop mixed taglines that acknowledge both positive and negative aspects of each category. These taglines should reflect both the strengths and weaknesses of the product category for each aspect. For example, "{X} praised the paper quality, but {Y} thought it was too thin","{X} appreciated the ink absorption, but {Y} encountered issues", "{X} liked the hole strength, but {Y} found it insufficient".
                        5. Include Synonyms: Provide synonyms for each aspect to enhance understanding and clarity. Synonyms could be alternative terms or phrases that convey the same meaning as the aspect. For example, "Paper Quality" could also be referred to as "Texture" or "Thickness".
                        6. Create the json: Organize all the information into a structured json format. Include keys for the category slug, aspects, positive taglines, mixed taglines, and synonyms.
'''
                    },
                    {
                        "role": "user", 
                        "content":f'''Category Slug: full-car-covers''' 
                 },{
                        "role": "assistant", 
                        "content":'''[
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Material Quality",
        "Tagline (Positive)": "Praised for its high-quality material",
        "Aspect Explanation": "The durability and robustness of the cover's fabric. For example, being tear-resistant and long-lasting.",
        "Tagline (Mixed)": "{X} praised for its high-quality material, while {Y} found it wore out quickly.",
        "Synonyms": "Fabric Quality, Durability"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Fit",
        "Tagline (Positive)": "Liked the perfect fit",
        "Aspect Explanation": "How well the cover fits the car. For example, snug and secure without being too tight.",
        "Tagline (Mixed)": "{X} liked the perfect fit, but {Y} found it too loose.",
        "Synonyms": "Fitting, Size Accuracy"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Weather Protection",
        "Tagline (Positive)": "Appreciated the excellent weather protection",
        "Aspect Explanation": "How well the cover protects against various weather conditions. For example, rain, snow, and UV rays.",
        "Tagline (Mixed)": "{X} appreciated the excellent weather protection, though {Y} thought it was inadequate.",
        "Synonyms": "Climate Protection, Weather Resistance"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Ease of Use",
        "Tagline (Positive)": "Found it easy to put on and take off",
        "Aspect Explanation": "The simplicity of installing and removing the cover. For example, user-friendly design with clear instructions.",
        "Tagline (Mixed)": "{X} found it easy to put on and take off, while {Y} had difficulties.",
        "Synonyms": "Usability, Handling"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Breathability",
        "Tagline (Positive)": "Liked its breathability",
        "Aspect Explanation": "How well the cover allows moisture to escape. For example, preventing mold and mildew.",
        "Tagline (Mixed)": "{X} liked its breathability, but {Y} experienced condensation issues.",
        "Synonyms": "Ventilation, Airflow"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Scratch Resistance",
        "Tagline (Positive)": "Praised for its scratch resistance",
        "Aspect Explanation": "The cover's ability to prevent scratches on the car's surface. For example, soft interior lining.",
        "Tagline (Mixed)": "{X} praised for its scratch resistance, while {Y} noticed scratches.",
        "Synonyms": "Scratch Protection, Abrasion Resistance"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Security Features",
        "Tagline (Positive)": "Appreciated the added security features",
        "Aspect Explanation": "The inclusion of features to secure the cover. For example, lockable hems or straps.",
        "Tagline (Mixed)": "{X} appreciated the added security features, although {Y} found them ineffective.",
        "Synonyms": "Anti-Theft Features, Locking Mechanisms"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Storage Convenience",
        "Tagline (Positive)": "Liked the compact storage design",
        "Aspect Explanation": "How easy it is to store the cover when not in use. For example, folding into a small, manageable size.",
        "Tagline (Mixed)": "{X} liked the compact storage design, but {Y} found it bulky.",
        "Synonyms": "Storage Ease, Portability"
    },
    {
        "Category Slug": "full-car-covers",
        "Aspect": "Waterproof",
        "Tagline (Positive)": "Appreciated its waterproof feature",
        "Aspect Explanation": "The cover's ability to repel water and keep the car dry. For example, being fully waterproof.",
        "Tagline (Mixed)": "{X} appreciated its waterproof feature, but {Y} found it leaked.",
        "Synonyms": "Water Resistance, Moisture Protection"
    }
]''' 
                 },{
                        "role": "user", 
                        "content":f'''Category Slug: {category_name}''' 
                 },
                ],
            model="llama3-70b-8192",
        )

        # print(chat_completion.choices[0].message.content)
        outputs= chat_completion.choices[0].message.content
        final_response=str(outputs)
        json_string = re.sub(r'^[^\[]*\[', '[', final_response, 1)

        print(final_response)
        # Parse JSON string into a list of dictionaries
        data = json.loads(json_string)

        # Define CSV file name
        csv_file_name = 'llama_Aspect.csv'


        file_exists = os.path.isfile(csv_file_name)

        # Writing data to CSV
        with open(csv_file_name, mode='a', newline='') as csv_file:
            # Get the fieldnames from the first dictionary
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write header only if the file does not exist or is empty
            if not file_exists:
                writer.writeheader()

            # Write rows to the CSV file
            for item in data:
                writer.writerow(item)

        print(f"Data successfully written to {csv_file_name}")

        # print("FINAL RESPONSE: ", outputs)
 
        return final_response

if __name__ == "__main__":
    extractor = ReviewSnippets()
#     csv_file_name = 'llama_Aspect.csv'


#     file_exists = os.path.isfile(csv_file_name)

#     headers = [
#     "Category Slug",
#     "Aspect",
#     "Tagline (Positive)",
#     "Aspect Explanation",
#     "Tagline (Mixed)",
#     "Synonyms"
# ]

#     # Writing data to CSV
#     with open(csv_file_name, mode='w', newline='') as csv_file:
#         csv_writer = csv.writer(csv_file)
#         csv_writer.writerow(headers)
    
    # Get the fieldnames from the first dictionary
    # extractor.get_aspects("centrifugal-juicers")
    # categories = ["travel-packing-organizers", "usb-cables", "usb-hubs", "waist-packs", "wall-tabletop-picture-frames", "webcams", "wine-glasses", "wireless-bluetooth-speakers", "womens-athletic-outdoor-sandals-slides", "womens-bikini-sets", "womens-casual-dresses", "womens-down-jackets-parkas", "womens-jumpsuits", "womens-minimizer-bras", "womens-pullover-sweaters"]

    # " sports-nutrition-nitric-oxide-boosters", "carb-blockers-supplements", "multi-enzyme-nutritional-supplements", "l-glutamine-nutritional-supplements", "power-hedge-trimmers",

    # "full-car-covers", "landscape-path-lights", "turmeric-herbal-supplements", "dog-hip-joint-care", "vehicle-cargo-carriers", "dog-grooming-clippers", "portable-solar-chargers", "womens-boots", "mens-boots", "boomboxes", "training-collars", "joint-muscle-pain-relief-rubs", "cd-players", "car-wax", "mens-rotary-shavers", "walking-canes", "dog-probiotic-supplements", "table-fans", "mens-water-shoes", "camping-chairs","traction-equipment", "car-seat-head-body-supports", "portable-dvd-players", "body-weight-scales-digital", "home-audio-subwoofers", "laptop-bags", "exterior-paint", "fishing-rods", "bassinets",

    categories = ["sporting-optics-mounts", "high-chair", "projection-screens", "hunting-shooting-earmuffs", "kids-tricycles", "coq10-nutritional-supplements", "exterior-care-products", "automotive-bug-sap-tar-removers", "Chrome & Metal Polishes", "Cleaners", "hiking-daypacks", "omega-3-6-9-oil-nutritional-supplements", "space-heaters", "roasted-coffee-beans","standard-baby-strollers", "psyllium-nutritional-supplement"]

    # categories = ["power-hedge-trimmers"]
    for category in categories:
        final_response = extractor.get_aspects(category)