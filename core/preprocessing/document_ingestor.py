import os
from core.preprocessing.pdf_loader import load_pdf

def ingest_documents(data_folder = "data"):
    
    all_documents = []
    
    for file_name in os.listdir(data_folder):
        
        if file_name.endswith(".pdf"):
            file_path = os.path.join(data_folder, file_name)
            print(f"Processing: {file_path}")
            pages = load_pdf(file_path)
            all_documents.extend(pages)
            
    return all_documents