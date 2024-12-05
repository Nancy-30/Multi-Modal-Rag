import os
from typing import Tuple, Union, List
import nltk
import speech_recognition as sr
from PyPDF2 import PdfReader
import pdfplumber

nltk.download("punkt", quiet=True)

def extract_text_from_pdf(file) -> str:
   
    extracted_text = ""

    try:
        try:
            pdf_reader = PdfReader(file)
            extracted_text += " ".join(
                [
                    page.extract_text()
                    for page in pdf_reader.pages
                    if page.extract_text()
                ]
            )
        except Exception as e:
            print(f"PyPDF2 extraction error: {e}")

        if not extracted_text:
            try:
                with pdfplumber.open(file) as pdf:
                    extracted_text += " ".join(
                        [
                            page.extract_text()
                            for page in pdf.pages
                            if page.extract_text()
                        ]
                    )
            except Exception as e:
                print(f"pdfplumber extraction error: {e}")

        return extracted_text.strip()

    except Exception as e:
        print(f"Comprehensive PDF extraction error: {e}")
        return ""


def extract_text_from_audio(file) -> str:
    
    try:
        file.seek(0)

        temp_audio_path = "temp_audio_file.wav"
        with open(temp_audio_path, "wb") as temp_file:
            temp_file.write(file.read())

        recognizers = [sr.Recognizer(), sr.Recognizer(), sr.Recognizer()]

        text_results = []

        try:
            with sr.AudioFile(temp_audio_path) as source:
                audio = recognizers[0].record(source)
                google_text = recognizers[0].recognize_google(audio)
                if google_text:
                    text_results.append(google_text)
        except Exception as e:
            print(f"Google Speech Recognition error: {e}")

        try:
            import whisper

            model = whisper.load_model("base")
            whisper_result = model.transcribe(temp_audio_path)
            if whisper_result and whisper_result["text"]:
                text_results.append(whisper_result["text"])
        except ImportError:
            print("Whisper not installed. Skipping.")
        except Exception as e:
            print(f"Whisper transcription error: {e}")

        os.remove(temp_audio_path)

        return " ".join(text_results) if text_results else ""

    except Exception as e:
        print(f"Comprehensive audio extraction error: {e}")
        return ""


def process_file(file) -> Tuple[str, Union[str, List[str]]]:

    file_type = file.name.split(".")[-1].lower()

    file.seek(0)

    try:
        if file_type == "pdf":
            text = extract_text_from_pdf(file)
            chunks = nltk.tokenize.sent_tokenize(text) if text else []
            return "pdf", chunks

        elif file_type == "txt":
            text = file.read().decode("utf-8")
            chunks = nltk.tokenize.sent_tokenize(text) if text else []
            return "txt", chunks

        elif file_type in ["wav", "m4a", "ogg"]:
            text = extract_text_from_audio(file)
            chunks = nltk.tokenize.sent_tokenize(text) if text else []
            return "audio", chunks

        else:
            return "unknown", "Unsupported file type"

    except Exception as e:
        print(f"File processing error for {file_type}: {e}")
        return "error", f"Error processing {file_type} file"
