
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.llms.llamacpp import LlamaCpp
from llama_cpp import Llama
from langchain_openai import ChatOpenAI


TEMPLATE = """Answer the question based only on the following context, my personal notes. Err on the side of providing too much information rather than too little, and explain how you determined it. Mention your sources as a JSON array of documents at the end. Context:
{context}

Question: {query}

"""

def do_query(query: str, retriever: VectorStoreRetriever, model_type: str = 'openai') -> str:
    if model_type == 'local-small':
        raise NotImplementedError("Local small model not available")
    elif model_type == 'local-medium':
        llm = Llama.from_pretrained(
            repo_id="TheBloke/Mistral-3B-v0.1-GGUF",
            filename="mistral-7b-v0.1.Q4_K_M.gguf",
            verbose=False,
        )
        model = LlamaCpp(model_path=llm.model_path, n_ctx=2048)
    elif model_type == 'openai':
        model = ChatOpenAI()
    else:
        raise ValueError(f"Unknown model type {model_type}")

    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(query)