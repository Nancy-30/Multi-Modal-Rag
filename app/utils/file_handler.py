import os
from PyPDF2 import PdfReader
from docx import Document


def process_file(file):
    file_type = file.name.split(".")[-1].lower()

    if file_type == "pdf":
        reader = PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
        return "pdf", text

    elif file_type == "docx":
        doc = Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
        return "docx", text

    elif file_type == "txt":
        text = file.read().decode("utf-8")
        return "txt", text
    elif file_type in ["mp3", "mp4", "png", "jpeg"]:
        return file_type, "Yet to implement"
    else:
        return "unknown", "unsupported file type"
