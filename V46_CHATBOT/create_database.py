from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# 1. Load PDFs
loader = PyPDFDirectoryLoader("pdfs")
documents = loader.load()

print("PDFs loaded:", len(documents))


# 2. Split PDF text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Text chunks created:", len(chunks))


# 3. Create embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# 4. Store in ChromaDB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("Database created successfully!")
