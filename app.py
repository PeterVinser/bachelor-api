from flask import Flask, request, jsonify

app = Flask(__name__)

def vector_based_retrieval(question):
    return {"answer": f"dummy vector answer for {question}", "context": []}

def graph_based_retrieval(question):
    return {"answer": f"dummy graph answer for {question}", "context": []}

def fusion_based_retrieval(question):
    return {"answer": f"dummy fusion answer for {question}", "context": []}

@app.route('/api/query', methods=['POST'])
def query():
    retrieval_type = int(request.headers.get('X-Retrieval-Type'))

    data = request.json
    question = data['question']

    if retrieval_type == 0:
        result = vector_based_retrieval(question)
    elif retrieval_type == 1:
        result = graph_based_retrieval(question)
    elif retrieval_type == 2:
        result = fusion_based_retrieval(question)
    else:
        return jsonify({"error": "Invalid retrieval type"}), 400
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)