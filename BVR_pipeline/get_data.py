import pandas as pd
import os
from datetime import datetime
 
excel_file_path = "/home/shtlp_0170/Desktop/BVR/BVR_pipeline/GS 2024 Content Team (1).xlsx"
top_20_sheet = "Top 20"
top_21_70_sheet = "Top 50 (21-70)"
 
# categories_list = ["menopause-medications-treatments", "window-air-conditioners","photosticks","plant-growing-lamps","keyboard-mouse-combos","dvd-players","headlight-bulbs","radios"]
# categories_list = ["home-office-desk-chairs","womens-flip-flops","fitness-trampolines","gun-sights","aromatherapy-diffusers","air-purifier"]
# categories_list = ["home-office-desk-chairs","womens-flip-flops","hdmi-cables","fitness-trampolines"]
# categories_list = ["window-air-conditioners", "room-air-conditioners", "photosticks", "plant-growing-lamps","home-office-desk-chairs"]
# categories_list=["vitamin-b-complex-supplements", "chest-freezers", "hand-blenders", "hepa-filter-air-purifiers", "muscle-stimulators-accessories","nail-polish"]
# categories_list= ["home-gyms", "personal-blenders", "hair-color", "canopies", "pc-gaming-keyboards", "computer-speakers", "sharpening-stones", "deck-sealer"]
# categories_list = ["split-system-air-conditioners", "womens-walking-shoes", "internal-power-supplies", "sewing-machines", "mens-sport-sandals-slides", "point-and-shoot-camera", "canister-vacuum-cleaners", "electric-breast-pumps", "yeast-infection-treatments"]
# categories_list=["sexual-enhancers", "drawing-markers", "polishing-waxing-kits", "Waxes", "adjustable-bed-bases"]
# categories_list = ["heart-rate-monitor", "external-cd-dvd-drives", "lash-enhancers-primers", "bedroom-mattresses", "mens-sandals", "mineral-drinking-water"]
# categories_list=["hair-loss-products", "power-strips", "wireless-audio-receivers-adapters", "garage-door-openers", "sonic-toothbrushes"]
# categories_list=["sonic-toothbrushes", "electric-induction-range", "steam-iron", "toothpaste", "diy-home-security-systems", "alarm-clocks", "dehydrators", "skillets", "facial-night-creams", "gymnastics-balance-beams-bases", "shampoos"]
# categories_list = ["adrenal-extract-nutritional-supplements", "coffee-makers", "external-hard-drives", "beard-mustache-trimmers", "outdoor-generators"]
# categories_list=['quadcopters-multirotors', 'insulated-bottles', 'earwax-removal', 'seat-covers-accessories', 'stereo-receivers']
# categories_list = ["room-air-purifiers", "knee-braces", "krill-oil-nutritional-supplements", "household-kitchen-stone-surface-cleaners", "cycling-bikes", "air-mattresses", "fish-oil-nutritional-supplements", "womens-road-running-shoes"]
# categories_list=["meat-grinders", "sofas-couches", "bed-pillows", "vitamin-b-complex-supplements", "chest-freezers", "hand-blenders", "hepa-filter-air-purifiers", "muscle-stimulators-accessories", "nail-polish", "body-hair-groomers", "personal-fans", "power-dental-flossers", "electric-bicycles", "gaming-chairs", "cat-odor-stain-removers"]
# categories_list=["air-purifier", "antinausea-treatments", "cat-flea-drops", "creatine-nutritional-supplements", "skin-care-sets-kits", "convection-ovens"]
# categories_list=["managerial-chairs-executive-chairs", "meat-thermometer", "desktop-label-printers", "mct-oil-nutritional-supplements", "flavonoid-vitamin-supplements", "tattoo-aftercare-products", "loafers-slip-ons", "strength-training-equipment", "full-sized-blenders"]
# categories_list=["menopause-medications-treatments", "modem-router-combos", "plant-growing-lamps", "headlight-bulbs", "womens-flip-flops", "all-purpose-cleaners", "gun-holsters", "self-cleaning-cat-litter-boxes", "hdmi-cables", "fitness-trampolines", "travel-systems", "gun-sights", "aromatherapy-diffusers", "air-purifier", "antinausea-treatments"]
# categories_list=["insulated-bottles", "mens-athletic-shoes", "compact-refrigerator", "walk-behind-lawn-mowers", "baseball-infielders-mitts", "portable-cd-players", "dog-flea-collars", "tactical-flashlights", "walkie-talkies", "core-abdominal-trainers"]
# categories_list=["bedroom-matresses", "gaming-chairs", "kyeboard-mouse-combos", "mens-athletic-shoes", "shampoos", "steam-iron", "vitamin-b-complex-supplements", "window-air-conditioners"]
# categories_list = ["bullet-surveillance-cameras","full-sized-blenders", "polishing-waxing-kits"]
# categories_list = ["bicycle-car-racks", "ginkgo-biloba-herbal-supplements", "prenatal-vitamins", "hair-masks"]
# categories_list = ["billiard-cue-sticks","beard-conditioners-oils", "mens-hiking-boots", "mens-sports-polo-shirts","audio-video-turntables", "mens-undershirts", "mugs"]
# categories_list = ["aaa-batteries", "airbrush-sets"]
# categories_list = ["loafers-slip-ons"]
# categories_list = ["wireless-bluetooth-speakers"]
# categories_list = ["compact-dryers", "scooters", "l-glutamine-nutritional-supplements", "single-serve-coffee-maker", "sports-water-bottles", "power-hedge-trimmers", "crib-mattresses", "pest-control-traps", "back-seat-cushions", "deadbolts"]
# categories_list = ["mens-hiking-boots"]
# , "programmable-thermostats", "full-car-covers"
# categories_list = ["dog-hip-joint-care", "vehicle-cargo-carriers", "dog-grooming-clippers", "programmable-thermostats", "full-car-covers"]
# categories_list = ["rowing-machines", "portable-generators", "fishing-reels"]
# categories_list= ["motor-oils", "swimming-pool-stain-removers", "dishwasher", "spray-air-fresheners", "all-in-ones-desktop"]
# categories_list = ["artificial-plants-greenery", "artificial-trees", "automotive-air-fresheners", "automotive-clips", "automotive-fender-flares", "automotive-upholstery-care-products", "bakery-take-out-containers", "ballpoint-pens", "barbecue-sauces", "barbecue-tool-sets"]
# , "barware-tool-sets", "bath-rugs"
# categories_list = ["barware-tool-sets", "bath-rugs", "beneficial-pest-control-insects", "bento-boxes", "billiard-cue-sticks", "binder-index-dividers", "body-repair-putty"]
# categories_list= ["bug-zappers", "building-toys", "camping-hammocks"]
categories_list = ["collectible-trading-card-albums"]
df_top_20 = pd.read_excel(excel_file_path, sheet_name=top_20_sheet)
df_top_21_70 = pd.read_excel(excel_file_path, sheet_name=top_21_70_sheet)
 
# Filter data based on categories list
filtered_data = []
 
for category in categories_list:
    # Check in 'Top 20' sheet
    top_20_filtered = df_top_20[df_top_20['category_slug'] == category][['category_slug', 'ASIN']]
    filtered_data.append(top_20_filtered)
    
    # Check in 'Top 21-70' sheet
    top_21_70_filtered = df_top_21_70[df_top_21_70['category_slug'] == category][['category_slug', 'ASIN']]
    filtered_data.append(top_21_70_filtered)
 
result_df = pd.concat(filtered_data)
 
# Save to CSV with current date
 
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
 
output_csv_file_path = os.path.join(output_folder, f"dataset_{datetime.now().strftime('%Y-%m-%d')}_2.csv")
result_df.to_csv(output_csv_file_path, index=False)
 
print(f"Data saved to {output_csv_file_path}")