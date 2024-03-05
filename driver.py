from pathlib import Path
from notes_rag import generate_retriever, do_query


path = Path("/Users/eswan18/Library/Mobile Documents/iCloud~md~obsidian/Documents/Ethan's Vault")


retriever = generate_retriever(path)
result = do_query(
    query="what's my name?",
    retriever=retriever,
    model_type='openai',
)
print(f'result = {result}')
