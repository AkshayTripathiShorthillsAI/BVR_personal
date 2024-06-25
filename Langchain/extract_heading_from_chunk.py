import re
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from typing import List, Tuple

# Example text with headings
text = """
# Introduction
Welcome to the document. This section provides an overview of the contents and sets the stage for the topics discussed.

# Chapter 1: The Beginning
In the beginning, there was only chaos. This chapter delves into the origins and the early stages of development.
More details and historical context are provided.

# Chapter 2: The Middle Ages
The middle ages were a time of great change. This section covers the key events and figures that shaped this era.
Important battles, cultural shifts, and technological advancements are highlighted.

# Chapter 3: The Modern Era
The modern era represents a period of rapid progress. This chapter explores the innovations and movements that define the contemporary world.
Focus is placed on significant discoveries and their impacts on society.

# Conclusion
In conclusion, this document has covered the journey from ancient times to the present. The main points are summarized, and future outlooks are discussed.
"""

# Function to chunk text under each heading
def chunk_text_with_headings(text: str, chunk_size: int = 200) -> List[Tuple[str, str]]:
    # Regex to find headings and their corresponding text
    pattern = re.compile(r"(# .+?)\n((?:.|\n)*?)(?=\n# |$)", re.DOTALL)
    matches = pattern.findall(text)
    
    chunks = []

    # Process each match
    for match in matches:
        heading, body = match
        heading = heading.strip().replace('# ', '')

        # Initialize the text splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=20
        )
        
        # Chunk the body text
        chunked_body = splitter.split_text(body.strip())

        # Append the chunks with their corresponding headings
        for chunk in chunked_body:
            chunks.append((heading, chunk))

    return chunks

# Chunk the text
chunks = chunk_text_with_headings(text)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare documents for FAISS
documents = [{"text": chunk, "metadata": {"heading": heading}} for heading, chunk in chunks]

# Create embeddings for the documents
doc_texts = [doc['text'] for doc in documents]
doc_embeddings = model.encode(doc_texts)

# Initialize FAISS index
d = doc_embeddings.shape[1]  # Dimension of embeddings
index = faiss.IndexFlatL2(d)  # Create a flat (CPU) index

# Add document embeddings to the index
index.add(doc_embeddings)

# Function to search the FAISS index
def search_faiss(query: str):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k=5)
    found = False
    for idx in I[0]:
        if idx != -1:  # Check if the index is valid
            chunk_text = documents[idx]['text']
            heading = documents[idx]['metadata']['heading']
            if query.lower() in chunk_text.lower():
                print(f"The input text falls under the heading: {heading}")
                print(f"Chunk: {chunk_text}\n")
                found = True
                break
    if not found:
        print("No relevant chunk found.")

# Loop to input text and perform similarity search
while True:
    user_input = input("Enter text (type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    
    search_faiss(user_input)
