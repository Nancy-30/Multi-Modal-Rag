import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class ResponseGenerator:
    def __init__(self):
        
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        except Exception as e:
            print(f"Model initialization error: {e}")
            raise

    def generate_response(self, 
                           data: str, 
                           query: str, 
                           max_tokens: int = 500) -> str:
        
        if data == "No relevant data found":
            return "Sorry, I couldn't find any relevant information to answer your query."

        prompt = f"""
        Context: {data}
        Query: {query}

        Provide a comprehensive, precise, and well-structured response based on the given context and query.
        """

        try:
            response = self.model.generate_content(
                prompt, 
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens
                )
            )
            
            return response.text if response.text.strip() else "Unable to generate a response."
        
        except Exception as e:
            print(f"Response generation error: {e}")
            return "An error occurred while generating the response. Please try again."