import streamlit as st
from utils.file_handler import process_file
from utils.retriever import SemanticRetriever
from utils.generator import ResponseGenerator


def main():
    st.title("Multimodal Knowledge Retrieval")

    retriever = SemanticRetriever()
    generator = ResponseGenerator()

    upload_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt", "wav"],
        help="Supports PDF, DOCX, TXT, Audio, and Image files",
    )

    if upload_file:
        try:
            file_type, content = process_file(upload_file)
            st.success(f"Successfully processed {file_type.upper()} file")

            query = st.text_input("Ask a question about the document")

            if query and content:
                with st.spinner("Searching for relevant information..."):
                    retrieved_data = retriever.retrieve_data(
                        chunks=content if isinstance(content, list) else [content],
                        query=query,
                    )

                with st.spinner("Generating response..."):
                    response = generator.generate_response(retrieved_data, query)

                st.subheader("Response")
                st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please try uploading a different file.")


if __name__ == "__main__":
    main()
