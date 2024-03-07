import sys
from pathlib import Path

from .prompt import do_query
from .store import generate_retriever

def query():
    if len(sys.argv) < 2:
        print("Missing path argument")
        sys.exit(1)
    path = Path(sys.argv[1])

    print("Creating retriever...")
    retriever = generate_retriever(path)

    while True:
        query = input("Query: ")
        print("----- Result ----")
        result = do_query(query, retriever, model_type="openai")
        print(result)