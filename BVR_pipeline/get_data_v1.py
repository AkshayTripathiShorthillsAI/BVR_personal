import pandas as pd
import os
from datetime import datetime
 
excel_file_path = "/home/shtlp_0170/Desktop/BVR/BVR_pipeline/Golden set - events.xlsx"
updated_sheet = "Updated"
sheet1 = "Sheet1"
 
# categories_list = ["artificial-plants-greenery", "artificial-trees", "automotive-air-fresheners", "automotive-clips", "automotive-fender-flares", "automotive-upholstery-care-products", "bakery-take-out-containers", "ballpoint-pens", "barbecue-sauces", "barbecue-tool-sets"]
# categories_list = ["barware-tool-sets", "bath-rugs", "beneficial-pest-control-insects", "bento-boxes", "billiard-cue-sticks", "binder-index-dividers", "body-repair-putty"]
categories_list = ["bug-zappers", "building-toys", "camping-hammocks"]
categories_list = ["coat-hangers"]
# , "bug-zappers"

df_updated = pd.read_excel(excel_file_path, sheet_name=updated_sheet)
df_sheet1 = pd.read_excel(excel_file_path, sheet_name=sheet1)
 

# Filter data based on categories list
filtered_data = []
 
for category in categories_list:
    updated_filtered = df_updated[df_updated['category_slug'] == category][['category_slug', 'ASIN']]
    filtered_data.append(updated_filtered)
    
    sheet1_filtered = df_sheet1[df_sheet1['category_slug'] == category][['category_slug', 'ASIN']]
    filtered_data.append(sheet1_filtered)
 
result_df = pd.concat(filtered_data)
 
# Save to CSV with current date
 
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
 
output_csv_file_path = os.path.join(output_folder, f"dataset_{datetime.now().strftime('%Y-%m-%d')}.csv")
result_df.to_csv(output_csv_file_path, index=False)
 
print(f"Data saved to {output_csv_file_path}")   


# categories_list=["bedroom-matresses", "gaming-chairs", "kyeboard-mouse-combos", "mens-athletic-shoes", "shampoos", "steam-iron", "vitamin-b-complex-supplements", "window-air-conditioners"]
# categories_list = ["bullet-surveillance-cameras","full-sized-blenders", "polishing-waxing-kits"]
# categories_list = ["bicycle-car-racks", "ginkgo-biloba-herbal-supplements", "prenatal-vitamins", "hair-masks"]
# categories_list = ["aaa-batteries", "airbrush-sets", "bark-collars", "flood-security-lights", "electric-razor"]
# categories_list =["hair-cutting-shears", "nail-growth-products"]
# categories_list = ["billiard-cue-sticks","beard-conditioners-oils", "mens-hiking-boots", "mens-sports-polo-shirts","audio-video-turntables", "mens-undershirts", "mugs"]
# categories_list = ["insulated-tumblers"]
# categories_list = ["novelty-coffee-mugs", "fruit-leathers", "fruit-snacks", "round-ring-binders", "wooden-colored-pencils", "kids-crayons", "drawing-crayons", "project-folders", "file-jackets-file-pockets" ,"liquid-highlighters", "flavored-drinking-water", "lunch-bags"]
# categories_list = ["loafers-slip-ons"]