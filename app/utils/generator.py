def generate_response(data):
    if data == "No relevant data found":
        return "Sorry, I couldn't find any relevant information."
    return f"Response : {data[:200]}..."
