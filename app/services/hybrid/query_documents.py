from flask import jsonify
import os
import weaviate
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from openai import OpenAI

def handle_query(question):
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_HOST'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv('WEAVIATE_ADMIN_KEY')),
        headers={
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
    )

    response = client.collections.get("BachelorEntity").query.hybrid(
        query=question, alpha=0.6, limit=5
    )

    graph = Neo4jGraph()

    condition = []

    for entity in response.objects:
        id, type = entity.properties.get("entityId"), entity.properties.get("entityType")
        condition.append(f"(e:{type} AND e.id = '{id}')")

    where = " OR ".join(condition)

    query = f"""
    MATCH (e)-[:EXTRACTED_FROM]->(d:DocumentChunk)
    WHERE {where}
    WITH d.content AS content, d, COUNT(d) AS num_connections
    RETURN content, num_connections
    ORDER BY num_connections DESC
    LIMIT 3
    """

    result = graph.query(query)

    chunks = []

    for chunk in result:
        chunks.append(chunk.get('content'))

    context = '\n'.join(chunks)

    prompt = f"""
    You are a Weaviate Vector Database expert.
    Answer the question based only on the following context:
    {context}
    Question: {question}
    """

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            { "role": "system", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return jsonify({"answer": answer})