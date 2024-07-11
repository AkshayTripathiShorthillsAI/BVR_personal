
import pandas as pd
import os
from groq import Groq
import re 
from dotenv import load_dotenv
import csv
import json

class AspectGeneration:
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
    extractor = AspectGeneration()
    csv_file_name = 'llama_Aspect.csv'


    file_exists = os.path.isfile(csv_file_name)

    headers = [
    "Category Slug",
    "Aspect",
    "Tagline (Positive)",
    "Aspect Explanation",
    "Tagline (Mixed)",
    "Synonyms"
]

    # Writing data to CSV
    with open(csv_file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)
    
    # Get the fieldnames from the first dictionary

    categories = ["household-ventilation-fans", "electric-knives-slicers", "masticating-juicers", "blu-ray-player", "roller-skates", "satchel-handbags-wallets", "contact-grills", "horny-goat-weed-herbal-supplements", "cell-phone-cases", "trench-rain", "centrifugal-juicers", "range-accessories", "bcaas", "spotlights", "fixed-blade-hunting-knives", "3v-batteries", "9v-batteries", "acetaminophen", "acidophilus-nutritional-supplements", "action-figures", "adults-paint-by-number-kits", "advent-calendars", "after-sun-skin-care", "allergy-medicine", "almonds", "medical-anatomy-books", "aquarium-filter-accessories", "aromatherapy-candles", "art-paints", "automotive-interior-mirrors", "automotive-interior-rearview-mirrors", "automotive-paint-kits", "automotive-top-coats", "automotive-windshield-snow-covers", "baby-bath-hooded-towels", "baby-bathing-products", "baby-bibs-burp-cloths-sets", "baby-body-wash", "baby-bottle-nipples", "baby-bottles", "baby-boys-bodysuits", "baby-boys-boots", "baby-boys-costumes", "baby-boys-one-piece-footies", "baby-boys-one-piece-rompers", "baby-boys-socks", "feeding", "baby-gift-sets", "baby-girls-blanket-sleepers", "baby-girls-bodysuits", "baby-girls-boots", "baby-girls-costumes", "baby-girls-one-piece-rompers", "baby-shampoo", "baby-sleep-soothers", "baking-parchment", "bike-handlebars", "black-tea", "board-games", "lotions", "bottled-iced-tea", "boys-costume-masks", "boys-costumes", "boys-fashion-hoodies-sweatshirts", "butter-warmers", "camcorders", "camera-batteries", "camping-folding-knives", "candy-chocolate-bars", "canned-dog-food", "cat-dental-care", "cell-phone-grips", "mobile-screen-protector", "cell-phone-stands", "chewing-gum", "chlorella-herbal-supplements", "chocolate-cookies", "christmas-ball-ornaments", "christmas-garlands", "christmas-trees", "citrus-juicers", "cleaning-brushes-dusters", "clothes-drawer-organizers", "collectible-card-game-booster-packs", "concealers-neutralizing-makeup", "continuous-output-lighting", "cosmetic-bags", "craft-glitter", "cranberry-herbal-supplements", "crochet-kits", "cutting-boards", "decorative-hanging-ornaments", "decorative-outdoor-lighting-projectors", "deodorants", "diaper-creams", "diaper-disposal-bags", "dishwasher-detergent"]

    # for category in categories:
    #     final_response = extractor.get_aspects(category)
    failed_categories = []

    for category in categories:
        attempts = 0
        while attempts < 5:
            try:
                extractor.get_aspects(category)
                break
            except Exception as e:
                print(f"Error processing category '{category}' on attempt {attempts + 1}: {e}")
                attempts += 1
                if attempts == 5:
                    failed_categories.append(category)
                continue

    print("The following categories failed after 5 attempts:")
    print(failed_categories)