import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_response(data, query):

    if data == "No relevant data found":
        return "Sorry, I couldn't find any relevant information."

    prompt = f"""
    Context : {data}
    Query : {query}

    Based on the given context and query, please provide a comprehensive and precise response.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "An error occurred while generating the response."
