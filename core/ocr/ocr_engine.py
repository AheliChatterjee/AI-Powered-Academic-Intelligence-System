from pdf2image import convert_from_path
import easyocr


reader = easyocr.Reader(['en'])


POPPLER_PATH = r"C:\poppler\poppler-24.08.0\Library\bin"


def extract_text_with_ocr(pdf_path):

    extracted_pages = []

    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    for page_number, image in enumerate(pages, start=1):

        image_path = f"temp_page_{page_number}.jpg"

        image.save(image_path, "JPEG")

        results = reader.readtext(image_path)

        page_text = ""

        for result in results:

            detected_text = result[1]

            page_text += detected_text + " "

        extracted_pages.append(
            {
                "page": page_number,
                "text": page_text.strip()
            }
        )

    return extracted_pages