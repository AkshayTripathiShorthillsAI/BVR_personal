# Import the datasets library
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023")

# Display some information about the dataset
print(dataset)

# Access a specific split of the dataset, e.g., the 'train' split
train_dataset = dataset['train']

# Display the first few examples from the train dataset
print(train_dataset[:5])
