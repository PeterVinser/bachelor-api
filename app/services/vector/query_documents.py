from flask import jsonify
from app.services.vector_store import VectorStore
from app.services.answer_generator import AnswerGenerator

def handle_query(question, temperature):
    with VectorStore() as store:
        chunks, chunk_ids = store.retrieve_chunks_content(question, k=6)

    context = '\n'.join(chunks)

    answer = AnswerGenerator(temperature).answer(question, context)

    return jsonify({"answer": answer, "context": chunk_ids})