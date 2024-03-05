from pathlib import Path
from notes_rag.main import load_documents


path = Path("/Users/eswan18/Library/Mobile Documents/iCloud~md~obsidian/Documents/Ethan's Vault")


documents = load_documents(path)
