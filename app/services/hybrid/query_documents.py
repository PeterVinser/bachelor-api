from flask import jsonify

def handle_query(question):
    return jsonify({"answer": "test"})