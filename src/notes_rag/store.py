from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever


CHUNK_SIZE = 500


def generate_retriever(path: Path, glob: str = "**/*.md") -> VectorStoreRetriever:
    store = generate_data_store(path, glob=glob)
    return store.as_retriever()


def generate_data_store(path: Path, glob: str = "**/*.md") -> FAISS:
    documents = _load_documents(path, glob=glob)
    print(f"Chunking {len(documents)} documents")
    chunks = _split_text(documents)
    print(f"Chunked into {len(chunks)} chunks")
    print(f"Generating FAISS data store")
    store = FAISS.from_documents(chunks, embedding=SentenceTransformerEmbeddings())
    print("Done generating data store")
    return store


def _load_documents(path: Path, glob: str) -> list[Document]:
    print(f"Loading documents from {path} with glob {glob}")
    loader = DirectoryLoader(path, glob=glob)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")
    return documents


def _split_text(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_SIZE // 2,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks