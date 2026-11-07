import os
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

if __name__ == "__main__":
    print("Ingesting...")
    loader = UnstructuredLoader(file_path="/Users/James/Desktop/Programming/Medium-Analyzer-RAG/mediumblogpost.txt", chunking_strategy="basic", max_characters=1000000)  # Set max_characters to a large value to load the entire file as a single document.
    #encoding="utf-8"
    documents = loader.load() # This will now load the entire file as a single document.
    print("splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print(f"created {len(texts)} chunks")


    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    print("ingesting...")
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME"]
    )
    print("finish")
    