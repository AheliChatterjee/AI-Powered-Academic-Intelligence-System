from pypdf import PdfReader
import os

from core.preprocessing.text_cleaner import clean_text

def load_pdf(file_path):

    reader = PdfReader(file_path)

    extracted_pages = []

    file_name = os.path.basename(file_path)

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()
        

        if text:
            cleaned_text = clean_text(text)
            
            extracted_pages.append(
                {
                    "page": page_number,
                    "source_document": file_name,
                    "text": cleaned_text
                }
            )

    return extracted_pages