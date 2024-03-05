from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.llms.llamacpp import LlamaCpp
from llama_cpp import Llama


TEMPLATE = """Answer the question based only on the following context:
{context}

Question: {query}

"""

def do_query(query: str, retriever: VectorStoreRetriever) -> str:
    llm = Llama.from_pretrained(
        # repo_id="Qwen/Qwen1.5-0.5B-Chat-GGUF",
        repo_id="mistralai/Mistral-7B-v0.1",
        device_map="auto",
        verbose=False
    )
    model = LlamaCpp(model_path=llm.model_path)
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)