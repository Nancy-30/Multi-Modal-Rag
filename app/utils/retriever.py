from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer, util

class SemanticRetriever:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            raise

    def retrieve_data(self, 
                      chunks: List[str], 
                      query: str, 
                      similarity_threshold: float = 0.1,
                      top_k: int = 3) -> Union[str, List[str]]:
       
        if not chunks or not query:
            return "No relevant data found"
        
        try:
            chunk_embeddings = self.model.encode(chunks, convert_to_tensor=False)
            query_embedding = self.model.encode(query, convert_to_tensor=False)

            similarities = [
                util.cos_sim(query_embedding, chunk_embed).item() 
                for chunk_embed in chunk_embeddings
            ]
            
            similarities = np.array(similarities)
            relevant_indices = np.argsort(similarities)[::-1]
                
            top_chunks = [
                chunks[idx] for idx in relevant_indices 
                if similarities[idx] > similarity_threshold
            ][:top_k]
            
            if top_chunks:
                return " ".join(top_chunks) if len(top_chunks) > 1 else top_chunks[0]
            
            return "No relevant data found"
        
        except Exception as e:
            print(f"Retrieval error: {e}")
            return "No relevant data found"