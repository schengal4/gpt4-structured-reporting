
from docx import Document
import fitz # Here's the link to the license of the library: https://www.gnu.org/licenses/agpl-3.0.html
from io import BytesIO
import pandas as pd
import json
import streamlit as st

def read_docx(file):
    with BytesIO(file.read()) as doc_file:
        document = Document(doc_file)
        result = "\n".join([para.text for para in document.paragraphs])
        return result
def text_from_pdf_file(pdf_file):
    # Limitations:  Only works for PDFs with text, not images.
    # Can't properly processing footers and headers.
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text

def text_from_pdf_file_path(pdf_file_path):
    # Limitations: Only works for PDFs with text, not scanned images.
    # Might not properly process footers and headers.
    with fitz.open(pdf_file_path) as doc:  # Use the file path directly
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text
# Assuming json_str is the JSON string
def convert_json_to_table(json_str):
    # Parse the JSON string to a Python data structure
    data = json.loads(json_str)
    
    # Convert the data to a pandas DataFrame
    df = pd.json_normalize(data)
    return df