import csv
import json

x = '''[
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Comfort",
        "Tagline (Positive)": "Softness and plushness that provides ultimate comfort while sitting and relaxing",
        "Aspect Explanation": "How well the pillow supports the head and neck during use, including its softness, shape, and material",
        "Tagline (Mixed)": "{X} praised the comfort, though {Y} felt it could be softer",
        "Synonyms": "Cushioning, Softness"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Fabric Quality",
        "Tagline (Positive)": "Appreciated the fabric quality",
        "Aspect Explanation": "The quality of the fabric used. For example, being durable, soft, and pleasant to touch.",
        "Tagline (Mixed)": "{X} appreciated the fabric quality, while {Y} thought it was rough",
        "Synonyms": "Material, Fabric Durability"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Design",
        "Tagline (Positive)": "Liked the design",
        "Aspect Explanation": "The visual appeal and aesthetic design of the pillow. For example, having trendy patterns and colors.",
        "Tagline (Mixed)": "{X} liked the design, although {Y} found it too plain",
        "Synonyms": "Aesthetics, Appearance"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Stitching",
        "Tagline (Positive)": "Praised the stitching",
        "Aspect Explanation": "The quality and durability of the stitching. For example, ensuring the pillow remains intact over time.",
        "Tagline (Mixed)": "{X} praised the stitching, but {Y} noticed it unraveling",
        "Synonyms": "Sewing Quality, Seam Strength"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Shape Retention",
        "Tagline (Positive)": "Found it retains shape well",
        "Aspect Explanation": "How well the pillow maintains its shape after use. For example, not becoming flat or misshapen.",
        "Tagline (Mixed)": "{X} found it retains shape well, though {Y} saw it flattening",
        "Synonyms": "Resilience, Form Stability"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Versatility",
        "Tagline (Positive)": "Liked its versatility",
        "Aspect Explanation": "The ability to use the pillow in various settings. For example, suitable for couches, beds, and chairs.",
        "Tagline (Mixed)": "{X} liked its versatility, but {Y} found it limited",
        "Synonyms": "Multi-Purpose, Adaptability"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Colorfastness",
        "Tagline (Positive)": "Appreciated the colorfastness",
        "Aspect Explanation": "The resistance of the fabric color to fading or running. For example, maintaining vibrant colors after washing.",
        "Tagline (Mixed)": "{X} appreciated the colorfastness, while {Y} noticed fading",
        "Synonyms": "Dye Stability, Color Retention"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Filling Quality",
        "Tagline (Positive)": "Liked the filling quality",
        "Aspect Explanation": "The quality of the pillow's filling. For example, using materials that provide good support and comfort.",
        "Tagline (Mixed)": "{X} liked the filling quality, but {Y} found it lumpy",
        "Synonyms": "Stuffing, Interior Material"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Hypoallergenic",
        "Tagline (Positive)": "Praised its hypoallergenic nature",
        "Aspect Explanation": "The pillow's suitability for people with allergies. For example, using materials that prevent allergic reactions.",
        "Tagline (Mixed)": "{X} praised its hypoallergenic nature, although {Y} experienced issues",
        "Synonyms": "Allergy-Friendly, Non-Allergenic"
    },
    {
        "Category Slug": "throw-pillows",
        "Aspect": "Ease of Cleaning",
        "Tagline (Positive)": "Appreciated the ease of cleaning",
        "Aspect Explanation": "How simple it is to clean the pillow. For example, being machine washable or having a removable cover.",
        "Tagline (Mixed)": "{X} appreciated the ease of cleaning, while {Y} found it difficult",
        "Synonyms": "Maintenance, Care"
    }
]'''

# Parse JSON string into a list of dictionaries
data = json.loads(x)

# Define CSV file name
csv_file_name = 'llama_Aspects.csv'

# Writing data to CSV
with open(csv_file_name, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
    writer.writeheader()
    for item in data:
        writer.writerow(item)

print(f"Data successfully written to {csv_file_name}")
