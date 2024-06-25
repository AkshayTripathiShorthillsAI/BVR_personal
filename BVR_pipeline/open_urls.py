import webbrowser
 
# List of categories
categories =["travel-packing-organizers", "usb-cables", "usb-hubs", "waist-packs", "wall-tabletop-picture-frames", "webcams", "wine-glasses", "wireless-bluetooth-speakers", "womens-athletic-outdoor-sandals-slides", "womens-bikini-sets", "womens-casual-dresses", "womens-down-jackets-parkas", "womens-jumpsuits", "womens-minimizer-bras", "womens-pullover-sweaters", "womens-pumps-shoes", "womens-sports-bras", "womens-swimwear-cover-ups", "womens-tops-tees-blouses", "woodcase-lead-pencils"]
 
# Base URL
base_url = "https://staging.bestviewsreviews.com/"
 
# Open each category in a new browser tab
for category in categories:
    url = base_url + category.lower()
    webbrowser.open_new_tab(url)
 
print("Web pages have been opened in new tabs.")