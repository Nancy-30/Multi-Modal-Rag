from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_data(chunks, query):
    chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
    query_embeddings = model.encode(query, convert_to_tensor=True)

    similarities = util.cos_sim(query_embeddings, chunk_embeddings)[0]
    best_match_index = similarities.argmax().item()

    if similarities[best_match_index] > 0.1:
        return chunks[best_match_index]
    return "No relevant data found"
