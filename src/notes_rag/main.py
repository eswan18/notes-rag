from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document


def load_documents(path: Path, glob: str = "**/*.md") -> list[Document]:
    loader = DirectoryLoader(path, glob=glob)
    documents = loader.load()
    return documents

