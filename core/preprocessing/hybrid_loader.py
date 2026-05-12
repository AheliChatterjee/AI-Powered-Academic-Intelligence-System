import os

from langchain_community.document_loaders import PyPDFLoader

from core.ocr.ocr_engine import extract_text_with_ocr


MIN_TEXT_THRESHOLD = 100


def load_pdf_hybrid(pdf_path):

    print(f"\nProcessing: {pdf_path}")

    extracted_pages = []

    try:

        loader = PyPDFLoader(pdf_path)

        pages = loader.load()

        total_text = ""

        for page in pages:

            total_text += page.page_content.strip()

        # -------------------------
        # NORMAL TEXT PDF
        # -------------------------

        if len(total_text) > MIN_TEXT_THRESHOLD:

            print("Using Native Text Extraction")

            for index, page in enumerate(pages, start=1):

                extracted_pages.append(
                    {
                        "page": index,
                        "source_document": os.path.basename(pdf_path),
                        "text": page.page_content.strip(),
                        "extraction_method": "native"
                    }
                )

        # -------------------------
        # SCANNED PDF
        # -------------------------

        else:

            print("Using OCR Extraction")

            ocr_pages = extract_text_with_ocr(pdf_path)

            for page_data in ocr_pages:

                extracted_pages.append(
                    {
                        "page": page_data["page"],
                        "source_document": os.path.basename(pdf_path),
                        "text": page_data["text"],
                        "extraction_method": "ocr"
                    }
                )

    except Exception as e:

        print(f"OCR Fallback Triggered: {e}")

        ocr_pages = extract_text_with_ocr(pdf_path)

        for page_data in ocr_pages:

            extracted_pages.append(
                {
                    "page": page_data["page"],
                    "source_document": os.path.basename(pdf_path),
                    "text": page_data["text"],
                    "extraction_method": "ocr"
                }
            )

    return extracted_pages