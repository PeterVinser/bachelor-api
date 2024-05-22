from flask import jsonify
from langchain_openai import OpenAIEmbeddings
import numpy as np
from app.services.vector_store import VectorStore
from app.services.graph_store import GraphStore
from app.services.answer_generator import AnswerGenerator

def get_sorted_indices(question, relation_embeddings):
    query_embedded = OpenAIEmbeddings().embed_query(question)

    relation_vectors = np.array(relation_embeddings)
    query_vector = np.array(query_embedded)

    norms = np.linalg.norm(relation_vectors, axis=1, keepdims=True)
    normalized_vectors = relation_vectors / norms

    other_norm = np.linalg.norm(query_vector)
    normalized_other_vector = query_vector / other_norm

    cosine_similarities = np.dot(normalized_vectors, normalized_other_vector)

    sorted_indices = np.argsort(-cosine_similarities)

    return sorted_indices.astype(int)


def get_top_targets(question, entities, relation_embeddings, targets, k):
    sorted_indices = get_sorted_indices(question, relation_embeddings)

    counter = 0

    top_targets = []

    for i in sorted_indices:
        if counter == k:
            break

        target = targets[i]

        if target not in entities:
            counter += 1

            top_targets.append(target)

    return top_targets

def handle_query(question, temperature):
    with VectorStore() as store:
        entities = store.retrieve_entities(question, k=10)

    with GraphStore() as graph:
        embeddings, targets = graph.get_relation_embeddings_with_targets(entities)

    top_targets = get_top_targets(question, entities, embeddings, targets, k=10)

    entities.extend(top_targets)

    with GraphStore() as graph:
        chunks, chunk_ids = graph.get_most_connected_chunks(entities, k=6)
    
    context = '\n'.join(chunks)

    answer = AnswerGenerator(temperature).answer(question, context)

    response = jsonify({"answer": answer})

    response.headers['Chunk-Ids'] = str(chunk_ids)
    
    return response