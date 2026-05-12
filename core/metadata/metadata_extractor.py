from core.classification.document_classifier import classify_document
from core.classification.structure_parser import parse_document_structure


def extract_metadata(document_object):

    text = document_object["text"]

    classification_result = classify_document(text)

    structure_result = parse_document_structure(text)

    metadata = {

        "source_document": document_object["source_document"],

        "page": document_object["page"],

        "document_type": classification_result["document_type"],

        "classification_scores": classification_result["scores"],

        "chapters": structure_result["chapters"],

        "sections": structure_result["sections"],

        "questions": structure_result["questions"],

        "content": text
    }

    return metadata