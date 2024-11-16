import pdfplumber
import re
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = " ".join([page.extract_text() for page in pdf.pages])
    return text


def preprocess_text(text):
    return re.sub(r"\s+", " ", text)


def test_process_pdf():
    with open("full_text.md", "r") as file:
        return file.read()


def process_pdf(pdf):
    text = extract_text_from_pdf(pdf)
    clean_text = preprocess_text(text)
    return clean_text
