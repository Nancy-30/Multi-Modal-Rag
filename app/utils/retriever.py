from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_data(chunks, query):
    if not chunks or not query:
        return "No relevant data found"
    
    try:
        chunk_embeddings = model.encode(chunks, convert_to_tensor=False)
        query_embedding = model.encode(query, convert_to_tensor=False)

        similarities = []
        for chunk_embed in chunk_embeddings:
            sim = util.cos_sim(query_embedding, chunk_embed).item()
            similarities.append(sim)
        
        similarities = np.array(similarities)
        
        best_match_index = similarities.argmax()
        best_similarity = similarities[best_match_index]
        
        if best_similarity > 0.05:  # Very low threshold
            print(f"Best match found with similarity: {best_similarity}")
            return chunks[best_match_index]
        
        return "No relevant data found"
    
    except Exception as e:
        print(f"Error in retrieval: {e}")
        return "No relevant data found"