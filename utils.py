
from docx import Document
import fitz
from fpdf import FPDF
from io import BytesIO

def read_docx(file):
    with BytesIO(file.read()) as doc_file:
        document = Document(doc_file)
        result = "\n".join([para.text for para in document.paragraphs])
        Document.close()
        return result
def text_from_pdf_file(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text