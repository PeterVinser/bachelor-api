from flask import jsonify
import app.services.vector.query_documents as vector
import app.services.graph.query_documents as graph
import app.services.hybrid.query_documents as hybrid
import os

def validate_header(headers):
    required_variables = ["X-OpenAI-Key", "X-Weaviate-Key", "X-Neo4j-Password", "X-Neo4j-Uri", "X-Temperature"]

    for variable in required_variables:
        if headers.get(variable) is None:
            raise ValueError(f"{variable} is missing")

def set_env_variables(headers):
    os.environ["OPENAI_API_KEY"] = str(headers.get("X-OpenAI-Key"))
    os.environ["WEAVIATE_READONLY_KEY"] = str(headers.get("X-Weaviate-Key"))
    os.environ["NEO4J_URI"] = str(headers.get("X-Neo4j-Uri"))
    os.environ["NEO4J_PASSWORD"] = str(headers.get("X-Neo4j-Password"))

def handle_query(request):
    headers = request.headers

    try:
        validate_header(headers)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    set_env_variables(headers)
    
    temperature = float(headers.get("X-Temperature"))
    retrieval_type = int(headers.get('X-Retrieval-Type'))

    data = request.json
    question = data['question']

    match(retrieval_type):
        case 0:
            return vector.handle_query(question, temperature)
        case 1:
            return graph.handle_query(question, temperature)
        case 2:
            return hybrid.handle_query(question, temperature)

    return jsonify({"error": "Invalid retrieval type"}), 400