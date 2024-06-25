import re
from sentence_transformers import SentenceTransformer
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from typing import List, Tuple

# Function to load PDF and extract text with page numbers
def load_pdf(file_path: str) -> List[Tuple[int, str]]:
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_with_pages = []

    for i, page in enumerate(pages):
        # Assuming the page number is mentioned at the top
        text_lines = page.page_content.split("\n")
        page_number = i + 1
        text = "\n".join(text_lines)
        text_with_pages.append((page_number, text))
    
    return text_with_pages

# Function to split text into separate entries based on a pattern
def split_text_into_entries(text: str) -> List[str]:
    pattern = re.compile(r'\(\d+\)')  # Assuming each entry starts with a number in parentheses
    entries = pattern.split(text)
    entries = [entry.strip() for entry in entries if entry.strip()]
    return entries

# Function to chunk text under each heading, including page number
def chunk_text_with_headings(text_with_pages: List[Tuple[int, str]], chunk_size: int = 200) -> List[Tuple[str, str, int]]:
    chunks = []

    for page_number, text in text_with_pages:
        entries = split_text_into_entries(text)

        for entry in entries:
            # Regex to find headings and their corresponding text
            pattern = re.compile(r"(# .+?)\n((?:.|\n)*?)(?=\n# |$)", re.DOTALL)
            matches = pattern.findall(entry)

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

                # Append the chunks with their corresponding headings and page number
                for chunk in chunked_body:
                    chunks.append((heading, chunk, page_number))

    return chunks

# Load the PDF
file_path = '/home/shtlp_0015/Desktop/BVR/Langchain/budget_speech.pdf'
text_with_pages = load_pdf(file_path)
print("Text with Pages:", text_with_pages)

# Chunk the text
chunks = chunk_text_with_headings(text_with_pages)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare documents for FAISS
documents = [{"text": chunk, "metadata": {"heading": heading, "page_number": page_number}} for heading, chunk, page_number in chunks]

try:
    # Create embeddings for the documents
    doc_embeddings = model.encode(doc_texts)
    print("Shape of doc_embeddings:", doc_embeddings.shape) 

    # Initialize FAISS index
    d = doc_embeddings.sha
    pe[1]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)  # Create a flat (CPU) index

    # Add document embeddings to the index
    index.add(doc_embeddings)

except Exception as e:
    print("An error occurred while creating embeddings:")
    print(e)
    exit()

# Function to search the FAISS index
def search_faiss(query: str):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k=5)
    found = False
    for idx in I[0]:
        if idx != -1:  # Check if the index is valid
            chunk_text = documents[idx]['text']
            heading = documents[idx]['metadata']['heading']
            page_number = documents[idx]['metadata']['page_number']
            if query.lower() in chunk_text.lower():
                print(f"The input text falls under the heading: {heading} on page number: {page_number}")
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
