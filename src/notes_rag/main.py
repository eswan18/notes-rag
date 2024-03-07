import sys
from pathlib import Path

from .prompt import do_query
from .store import generate_retriever
from prompt_toolkit import PromptSession


def prompt():
    if len(sys.argv) < 2:
        print("Missing path argument")
        sys.exit(1)
    path = Path(sys.argv[1])

    print("Creating retriever...")
    retriever = generate_retriever(path)

    session = PromptSession()
    while True:
        try:
            query = session.prompt("Query: ")
        except EOFError:
            print("Exiting...")
            break
        print("----- Result ----")
        result = do_query(query, retriever, model_type="openai")
        print(result)
