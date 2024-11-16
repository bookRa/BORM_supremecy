import pdfplumber
import re
from openai import OpenAI
import os
from dotenv import load_dotenv
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import tempfile


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = " ".join([page.extract_text() for page in pdf.pages])
    return text

def extract_text_from_epub(epub_file):
    book = epub.read_epub(epub_file)
    text = ""
    for item in book.get_items():
        if item.get_type() == ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text() + " "
    return text


def preprocess_text(text):
    return re.sub(r"\s+", " ", text)


def test_process_pdf(pdf):
    with open("full_text.md", "r") as file:
        return file.read()


# def process_pdf(pdf):
#     text = extract_text_from_pdf(pdf)
#     clean_text = preprocess_text(text)
#     return clean_text

def process_document(file_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_path.name)[1]) as temp_file:
        temp_file.write(file_path.read())
        temp_file_path = temp_file.name

    if file_path.name.lower().endswith(".pdf"):
        raw_text = extract_text_from_pdf(temp_file_path)
    elif file_path.name.lower().endswith(".epub"):
        raw_text = extract_text_from_epub(temp_file_path)

    os.remove(temp_file_path)

    return preprocess_text(raw_text)