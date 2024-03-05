from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever


def generate_retriever(path: Path, glob: str = "**/*.md") -> VectorStoreRetriever:
    store = generate_data_store(path, glob=glob)
    return store.as_retriever()


def generate_data_store(path: Path, glob: str = "**/*.md") -> FAISS:
    documents = _load_documents(path, glob=glob)
    chunks = _split_text(documents)
    store = FAISS.from_documents(chunks, embedding=SentenceTransformerEmbeddings())
    return store


def _load_documents(path: Path, glob: str) -> list[Document]:
    loader = DirectoryLoader(path, glob=glob)
    documents = loader.load()
    return documents


def _split_text(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks