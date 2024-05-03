from flask import jsonify
import app.services.vector.query_documents as vector
import app.services.graph.query_documents as graph
import app.services.hybrid.query_documents as hybrid

def handle_query(request):
    retrieval_type = int(request.headers.get('X-Retrieval-Type'))

    data = request.json
    question = data['question']

    match(retrieval_type):
        case 0:
            return vector.handle_query(question)
        case 1:
            return graph.handle_query(question)
        case 2:
            return hybrid.handle_query(question)

    return jsonify({"error": "Invalid retrieval type"}), 400