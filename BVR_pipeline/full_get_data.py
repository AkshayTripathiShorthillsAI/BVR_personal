import pandas as pd
import os
from datetime import datetime
 
# excel_file_path_1 = "/home/shtlp_0170/Desktop/BVR/BVR_pipeline/Golden set - events.xlsx"
# excel_file_path_2 = "/home/shtlp_0170/Desktop/BVR/BVR_pipeline/GS 2024 Content Team (1).xlsx"
excel_file_path = "/home/shtlp_0170/Desktop/BVR/BVR_pipeline/GS 2024 Content Team (1).xlsx"
scrapped_asin_list = "Scrapped ASIN list"
# updated_sheet = "Updated"
# sheet1 = "Sheet1"
# top_20_sheet = "Top 20"
# top_21_70_sheet = "Top 50 (21-70)"
 
# categories_list = ["artificial-plants-greenery", "artificial-trees", "automotive-air-fresheners", "automotive-clips", "automotive-fender-flares", "automotive-upholstery-care-products", "bakery-take-out-containers", "ballpoint-pens", "barbecue-sauces", "barbecue-tool-sets"]
# categories_list = ["barware-tool-sets", "bath-rugs", "beneficial-pest-control-insects", "bento-boxes", "billiard-cue-sticks", "binder-index-dividers", "body-repair-putty"]
# categories_list = ["bug-zappers", "building-toys", "camping-hammocks"]
# categories_list = ["canned-cat-food", "card-games", "coffee-machines", "casual-daypacks", "cat-hair-removal-products", "cheese-servers", "clips"]
# categories_list = ["collectible-trading-card-albums"]
# categories_list = ["composition-notebooks", "computer-microphones", "construction-paper", "countertop-blenders", "crossbody-bags", "d-ring-binders", "dartboards", "dish-cloths-dish-towels", "disposable-diapers", "dog-beds"]
# categories_list = ["dog-chew-toys", "dog-grooming-wipes", "dog-hair-removal-products", "dog-toy-balls", "dog-treat-cookies-biscuits-snacks", "dog-wormers", "domino-tile-games", "drafting-tools-drafting-kits", "egg-slicers" , "electrical-multi-outlets"]
# categories_list = ["electrical-outlet-switches", "espresso-machine-coffeemaker-combos", "everyday-bras", "exercise-fitness-dumbbells", "eye-masks", "fabric-adhesives", "fabric-deodorizer", "face-mists", "facial-skin-care-sets-kits", "facial-sunscreens", "facial-toners-astringents", "fashion-hoodies-sweatshirts",]
# categories_list = [ "fitted-bed-sheets", "flatware-sets", "food-chopper", "food-container-sets","coat-hangers", "gel-ethanol-fireplaces", "gel-ink-pens","hair-brushes", "hair-curling-wands", "hair-styling-gels"]
# categories_list = ["hardcover-executive-notebooks", "hole-punches", "home-thermostat-accessories", "household-cleaning-sponges", "index-cards", "individual-household-food-containers", "jewelry-boxes-organizers", "kids-backpacks", "kids-crayons"]
# categories_list = ["carpet-upholstery-cleaning-machines","kids-lunch-bags", "kids-lunch-boxes", "kids-stickers", "kitchen-cookware-sets", "knife-sets", "laptop-chargers-adapters", "liquid-white-glues", "lunch-boxes", "mascara", "mattress-protectors", "mens-casual-button-down-shirts", "mens-cowboy-hats"]
# categories_list = ["throw-pillows", "centrifugal-juicers", "masticating-juicers", "food-chopper", "fat-burners"]
# categories_list = ["food-processor", "baby-stationary-activity-centers", "masticating-juicers", "womens-foil-shavers", "centrifugal-juicers", "food-chopper", "throw-pillows", "tongue-and-groove-pliers", "motorcycle-goggles", "ammunition-magazine-pouches", "fat-burners", "mens-henley-shirts"]

# Following are defected category 
# categories_list = ["mens-cross-training-shoes", "mens-electric-shaver-replacement-heads", "mens-loafers-slip-ons", "mens-novelty-socks", "mens-novelty-t-shirts", "mens-outerwear-vests", "mens-oxford-derby-boots", "mens-slippers", "mens-t-shirts", "mens-wrist-watches", "mixing-bowls", "motor-oils", "multitools"]
# categories_list = ["egg-slicers"]
# categories_list = ["egg-slicers","hardcover-executive-notebooks", "kids-stickers", "kitchen-cookware-sets", "knife-sets"]
# categories_list = ["liquid-white-glues", "mattress-protectors", "mens-cowboy-hats", "night-lights", "old-fashioned-glasses", "one-pieces-swimming-suit", "outdoor-fire-pits", "outdoor-string-lights", "patio-bistro-sets", "patio-umbrellas", "pen-pencil-marker-cases", "pencil-sharpeners", "permanent-markers-marker-pens", "personal-groomers", "personal-makeup-mirrors", "personal-size-blenders"]
# categories_list = ["pest-control-baits-lures", "photographic-film", "planners", "planning-boards", "plant-germination-kits", "platforms-wedges", "pool-safety-covers", "portfolio-case-ring-binders", "powersports-rain-jackets", "recording-headphone-audio-monitors", "repeaters", "reusable-lunch-bags", "sandwich-makers-panini-presses", "seasoning-spice-choppers", "self-stick-note-pads"]
# categories_list = ["shower-caddies", "sketchbooks-notebooks", "smart-speakers", "smartwatch-cables-chargers", "special-education-school-supplies"]
# categories_list = ["standard-pencil-erasers", "starch-anti-static-sprays", "swimming-pool-algaecides", "swimming-pool-balancers", "swimming-pool-chlorine", "swimming-pool-clarifiers-enzymes", "tanks-camis", "tool-belts", "trash-bags", "travel-duffel-bags"]
# categories_list = ["travel-packing-organizers", "usb-cables", "usb-hubs", "waist-packs", "wall-tabletop-picture-frames", "webcams", "wine-glasses", "wireless-bluetooth-speakers", "womens-athletic-outdoor-sandals-slides", "womens-bikini-sets", "womens-casual-dresses", "womens-down-jackets-parkas", "womens-jumpsuits", "womens-minimizer-bras", "womens-pullover-sweaters"]
categories_list = ["womens-minimizer-bras", "womens-pullover-sweaters", "womens-pumps-shoes", "womens-sports-bras", "womens-swimwear-cover-ups", "womens-tops-tees-blouses", "woodcase-lead-pencils"]
# categories_list = ["food-processor", "baby-stationary-activity-centers", "womens-foil-shavers", "tongue-and-groove-pliers", "motorcycle-goggles", "ammunition-magazine-pouches", "mens-henley-shirts", "mens-electric-shaver-replacement-heads", "mens-novelty-socks", "mens-novelty-t-shirts", "mens-t-shirts", "mens-wrist-watches", "motor-oils"]
# categories_list = ["food-processor", "baby-stationary-activity-centers", "womens-foil-shavers", "tongue-and-groove-pliers", "motorcycle-goggles", "ammunition-magazine-pouches", "mens-henley-shirts"]
# categories_list = [  " , "mens-electric-shaver-replacement-heads","neck-décolleté-moisturizers", "night-lights", "novelty-coffee-mugs", "old-fashioned-glasses", "one-pieces-swimming-suit", "outdoor-fire-pits", "outdoor-string-lights", "patio-bistro-sets", "patio-umbrellas", "pen-pencil-marker-cases", "pencil-sharpeners", "permanent-markers-marker-pens", "personal-groomers", "personal-makeup-mirrors", "personal-size-blenders", "pest-control-baits-lures", "photographic-film", "planners", "planning-boards", "plant-germination-kits", "platforms-wedges", "pool-safety-covers", "portable-generators", "portfolio-case-ring-binders", "powersports-rain-jackets", "programmable-thermostats", "project-folders", "recording-headphone-audio-monitors", "repeaters", "reusable-lunch-bags", "round-ring-binders", "rowing-machines", "sandwich-makers-panini-presses", "seasoning-spice-choppers", "self-stick-note-pads", "shower-caddies", "sketchbooks-notebooks", "smart-speakers", "smartwatch-cables-chargers", "special-education-school-supplies", "spray-air-fresheners", "standard-pencil-erasers", "starch-anti-static-sprays", "swimming-pool-algaecides", "swimming-pool-balancers", "swimming-pool-chlorine", "swimming-pool-clarifiers-enzymes", "swimming-pool-stain-removers", "tanks-camis", "tool-belts", "trash-bags", "travel-duffel-bags", "travel-packing-organizers", "usb-cables", "usb-hubs", "waist-packs", "wall-tabletop-picture-frames", "webcams", "wine-glasses", "wireless-bluetooth-speakers", "womens-athletic-outdoor-sandals-slides", "womens-bikini-sets", "womens-casual-dresses", "womens-casual-pants-capris", "womens-down-jackets-parkas", "womens-jumpsuits", "womens-minimizer-bras", "womens-pullover-sweaters", "womens-pumps-shoes", "womens-sports-bras", "womens-swimwear-cover-ups", "womens-tops-tees-blouses", "woodcase-lead-pencils", "wooden-colored-pencils"]
# df_updated = pd.read_excel(excel_file_path_1, sheet_name=updated_sheet)
# df_sheet1 = pd.read_excel(excel_file_path_1, sheet_name=sheet1)


# df_top_20 = pd.read_excel(excel_file_path_2, sheet_name=top_20_sheet)
# df_top_21_70 = pd.read_excel(excel_file_path_2, sheet_name=top_21_70_sheet)
 
df_scrapped_asin_list = pd.read_excel(excel_file_path, sheet_name=scrapped_asin_list)

filtered_data = []
 
for category in categories_list:
    scrapped_asin_list_filtered = df_scrapped_asin_list[df_scrapped_asin_list['category_slug'] == category][['category_slug', 'ASIN']]
    filtered_data.append(scrapped_asin_list_filtered)
    # updated_filtered = df_updated[df_updated['category_slug'] == category][['category_slug', 'ASIN']]
    # filtered_data.append(updated_filtered)
    
    # sheet1_filtered = df_sheet1[df_sheet1['category_slug'] == category][['category_slug', 'ASIN']]
    # filtered_data.append(sheet1_filtered)

    # top_20_filtered = df_top_20[df_top_20['category_slug'] == category][['category_slug', 'ASIN']]
    # filtered_data.append(top_20_filtered)

    # top_21_70_filtered = df_top_21_70[df_top_21_70['category_slug'] == category][['category_slug', 'ASIN']]
    # filtered_data.append(top_21_70_filtered)
 
result_df = pd.concat(filtered_data)
 
# Save to CSV with current date
 
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
 
output_csv_file_path = os.path.join(output_folder, f"dataset_{datetime.now().strftime('%Y-%m-%d')}.csv")
result_df.to_csv(output_csv_file_path, index=False)
 
print(f"Data saved to {output_csv_file_path}")   