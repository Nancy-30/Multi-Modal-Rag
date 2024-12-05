import streamlit as st
from utils.file_handler import process_file
from utils.retriever import SemanticRetriever
from utils.generator import ResponseGenerator

def main():
    st.set_page_config(
        page_title="Knowledge Retrieval",
        page_icon="🔍",
        layout="wide"
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
        }
        .main-header {
            color: #ffffff;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
        }
        .stButton button {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }
        .success-box {
            background-color: #2ecc71;
            padding: 10px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
        }
        .error-box {
            background-color: #e74c3c;
            padding: 10px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main Title
    st.markdown("<h1 class='main-header'>🔍 Multimodal Knowledge Retrieval</h1>", unsafe_allow_html=True)

    # Sidebar for file upload
    with st.sidebar:
        st.header("Upload Document")
        upload_file = st.file_uploader(
            "Choose a file",
            type=["txt", "wav", "docx", "pdf"],
            help="Supports TXT, WAV, DOCX, and PDF files"
        )
        st.markdown("💡 *Supported formats: TXT, WAV, DOCX, PDF*")

    # Main Section
    if upload_file:
        try:
            file_type, content = process_file(upload_file)

            # Success Message
            st.markdown(f"<div class='success-box'>Successfully processed {file_type.upper()} file</div>", unsafe_allow_html=True)

            query_container = st.container()
            with query_container:
                with st.form(key="query_form"):
                    query = st.text_input("❓ Ask a question about the document", placeholder="Type your query here...")
                    submit_button = st.form_submit_button(label="Submit")

                if submit_button and query and content:
                    with st.spinner("🔍 Searching for relevant information..."):
                        retriever = SemanticRetriever()
                        retrieved_data = retriever.retrieve_data(
                            chunks=content if isinstance(content, list) else [content],
                            query=query,
                        )

                    with st.spinner("💡 Generating response..."):
                        generator = ResponseGenerator()
                        response = generator.generate_response(retrieved_data, query)

                    st.subheader("Response")
                    st.write(response)

        except Exception as e:
            st.markdown(f"<div class='error-box'>An error occurred: {e}</div>", unsafe_allow_html=True)
            st.error("Please try uploading a different file.")
    else:
        st.info("📁 Upload a document to get started!")

if __name__ == "__main__":
    main()
