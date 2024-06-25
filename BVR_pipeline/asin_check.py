import csv

# Define the file paths
input_csv_path = '/home/shtlp_0170/Desktop/BVR/BVR_pipeline/output/dataset_2024-06-14_delete.csv'
output_csv_path = '/home/shtlp_0170/Desktop/BVR/BVR_pipeline/output/asin_not_found.csv'

# List of categories to check against
categories_list = ["all-in-ones-desktop", "art-paintbrush-sets", "artificial-plants-greenery", "artificial-trees", "audio-video-turntables", "automotive-air-fresheners", "automotive-clips", "automotive-fender-flares", "automotive-upholstery-care-products", "bakery-take-out-containers", "ballpoint-pens", "barbecue-sauces", "barbecue-tool-sets", "barware-tool-sets", "bath-rugs", "beard-conditioners-oils", "beneficial-pest-control-insects", "bento-boxes", "billiard-cue-sticks", "binder-index-dividers", "body-repair-putty", "bug-zappers", "building-toys", "camping-hammocks", "canned-cat-food", "card-games", "carpet-upholstery-cleaning-machines", "casual-daypacks", "cat-hair-removal-products", "cheese-servers", "clips", "coat-hangers", "coffee-machines", "collectible-trading-card-albums", "composition-notebooks", "computer-microphones", "construction-paper", "countertop-blenders", "crossbody-bags", "d-ring-binders", "dartboards", "dish-cloths-dish-towels", "disposable-diapers", "dog-beds", "dog-chew-toys", "dog-grooming-wipes", "dog-hair-removal-products", "dog-toy-balls", "dog-treat-cookies-biscuits-snacks", "dog-wormers", "domino-tile-games", "drafting-tools-drafting-kits", "drawing-crayons", "egg-slicers", "electrical-multi-outlets", "electrical-outlet-switches", "espresso-machine-coffeemaker-combos", "everyday-bras", "exercise-fitness-dumbbells", "eye-masks", "fabric-adhesives", "fabric-deodorizer", "face-mists", "facial-skin-care-sets-kits", "facial-sunscreens", "facial-toners-astringents", "fashion-hoodies-sweatshirts", "file-jackets-file-pockets", "fishing-reels", "fitted-bed-sheets", "flatware-sets", "flavored-drinking-water", "food-chopper", "food-container-sets", "fruit-leathers", "fruit-snacks", "gel-ethanol-fireplaces", "gel-ink-pens", "hair-brushes", "hair-curling-wands", "hair-styling-gels", "hardcover-executive-notebooks", "hole-punches", "home-thermostat-accessories", "household-cleaning-sponges", "index-cards", "individual-household-food-containers", "jewelry-boxes-organizers", "kids-backpacks", "kids-crayons", "kids-lunch-bags", "kids-lunch-boxes", "kids-stickers", "kitchen-cookware-sets", "knife-sets", "laptop-chargers-adapters", "liquid-highlighters", "liquid-white-glues", "lunch-bags", "lunch-boxes", "mascara", "mattress-protectors", "mens-casual-button-down-shirts", "mens-cowboy-hats", "mens-cross-training-shoes", "mens-electric-shaver-replacement-heads", "mens-hiking-boots", "mens-loafers-slip-ons", "mens-novelty-socks", "mens-novelty-t-shirts", "mens-outerwear-vests", "mens-oxford-derby-boots", "mens-slippers", "mens-sports-polo-shirts", "mens-t-shirts", "mens-undershirts", "mens-wrist-watches", "mixing-bowls", "motor-oils", "mugs", "multitools", "neck-décolleté-moisturizers", "night-lights", "novelty-coffee-mugs", "old-fashioned-glasses", "one-pieces-swimming-suit", "outdoor-fire-pits", "outdoor-string-lights", "patio-bistro-sets", "patio-umbrellas", "pen-pencil-marker-cases", "pencil-sharpeners", "permanent-markers-marker-pens", "personal-groomers", "personal-makeup-mirrors", "personal-size-blenders", "pest-control-baits-lures", "photographic-film", "planners", "planning-boards", "plant-germination-kits", "platforms-wedges", "pool-safety-covers", "portable-generators", "portfolio-case-ring-binders", "powersports-rain-jackets", "programmable-thermostats", "project-folders", "recording-headphone-audio-monitors", "repeaters", "reusable-lunch-bags", "round-ring-binders", "rowing-machines", "sandwich-makers-panini-presses", "seasoning-spice-choppers", "self-stick-note-pads", "shower-caddies", "sketchbooks-notebooks", "smart-speakers", "smartwatch-cables-chargers", "special-education-school-supplies", "spray-air-fresheners", "standard-pencil-erasers", "starch-anti-static-sprays", "swimming-pool-algaecides", "swimming-pool-balancers", "swimming-pool-chlorine", "swimming-pool-clarifiers-enzymes", "swimming-pool-stain-removers", "tanks-camis", "tool-belts", "trash-bags", "travel-duffel-bags", "travel-packing-organizers", "usb-cables", "usb-hubs", "waist-packs", "wall-tabletop-picture-frames", "webcams", "wine-glasses", "wireless-bluetooth-speakers", "womens-athletic-outdoor-sandals-slides", "womens-bikini-sets", "womens-casual-dresses", "womens-casual-pants-capris", "womens-down-jackets-parkas", "womens-jumpsuits", "womens-minimizer-bras", "womens-pullover-sweaters", "womens-pumps-shoes", "womens-sports-bras", "womens-swimwear-cover-ups", "womens-tops-tees-blouses", "woodcase-lead-pencils", "wooden-colored-pencils"]

# Initialize a set to keep track of unique category slugs from the CSV
csv_categories = set()

# Read the CSV file and extract category slugs
with open(input_csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        csv_categories.add(row['category_slug'])

# Find categories that are not in the CSV file
missing_categories = [category for category in categories_list if category not in csv_categories]

# Write the missing categories to a new CSV file
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['category_slug'])
    for category in missing_categories:
        csv_writer.writerow([category])

print(f"Missing categories have been written to {output_csv_path}")
