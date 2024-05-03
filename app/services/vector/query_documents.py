from flask import jsonify
import weaviate
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import os

def handle_query(question):
    
    client = weaviate.Client(
        url=os.getenv("WEAVIATE_HOST"),
        auth_client_secret=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_READONLY_KEY")),
        additional_headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )

    retriever = WeaviateHybridSearchRetriever(
        client=client,
        index_name="BachelorDocumentChunk",
        text_key="content",
        k=10,
        alpha=0.6
    )

    template = """
    You are a Weaviate Vector Database expert.
    Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # RAG
    model = ChatOpenAI(model='gpt-4-turbo-preview')

    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | prompt
        | model
        | StrOutputParser()
    )

    result = chain.invoke(question)

    return jsonify({"answer": result})