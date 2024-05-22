from flask import jsonify
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_community.graphs.neo4j_graph import Neo4jGraph
from langchain_core.prompts.prompt import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
EXTREMELY IMPORTANT: Remember not to use property DocumentName in your CYPHER query as it is a reserved property. Never use any reference to this property in any CYPHER queries.
Examples: Here are a few examples of generated Cypher statements for particular questions:
# What prize did Pierre Curie won?
MATCH (p:Person {{id:"Pierre Curie"}})-[:AWARD_WINNER]->(a:Award)
RETURN p, a

The question is:
{question}"""

def handle_query(question, temperature):

    CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
    )

    graph = Neo4jGraph()

    llm = ChatOpenAI(model='gpt-4o', temperature=0)
    qa_llm = ChatOpenAI(model="gpt-4o", temperature=temperature)
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, qa_llm=qa_llm, cypher_prompt=CYPHER_GENERATION_PROMPT, verbose=True)

    answer = chain.invoke({"query": question})

    return jsonify({"answer": answer["result"]})