import os
from PyPDF2 import PdfReader
from docx import Document
import nltk
import speech_recognition as sr

nltk.download("punkt")


def process_file(file):
    file_type = file.name.split(".")[-1].lower()

    if file_type == "pdf":
        print("pdf called")
        reader = PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
        chunks = nltk.tokenize.sent_tokenize(text)
        return "pdf", chunks

    elif file_type == "docx":
        doc = Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
        return "docx", text

    elif file_type == "txt":
        text = file.read().decode("utf-8")
        print("text : ", text)
        return "txt", text

    elif file_type in ["mp3", "wav"]:
        try:
            recognizer = sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                chunks = nltk.tokenize.sent_tokenize(text)
                print("working")
                return "audio", chunks
        except sr.UnknownValueError:
            print("audio not understand")
            return "audio", "Could not understand audio."
        except sr.RequestError as e:
            return (
                "audio",
                f"Could not request results from speech recognition service: {e}",
            )
        except Exception as e:
            return "audio", f"Error processing audio: {e}"

    elif file_type in ["mp4", "png", "jpeg"]:
        return file_type, "Yet to implement"
    else:
        return "unknown", "unsupported file type"
