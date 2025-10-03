import pdfplumber
import pandas as pd

def extract_pdf_text(file_like):
    text = ""
    with pdfplumber.open(file_like) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def read_excel(file_like):
    return pd.read_excel(file_like, sheet_name=None)  # dict of dfs
