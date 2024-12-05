import streamlit as st
from utils.file_handler import process_file
from utils.retriever import retrieve_data
from utils.generator import generate_response

st.title("Multimodal Rag System")

upload_file = st.file_uploader(
    "Upload a file ", type=["pdf", "docx", "txt", "mp3", "mp4", "png"]
)
if upload_file:
    file_type, content = process_file(upload_file)
    st.write(f"Processed file type : {file_type}")

    query = st.text_input("Ask your query")
    if query:
        retrieved_data = retrieve_data(content, query)
        response = generate_response(retrieved_data, query)
        st.write("Response", response)
