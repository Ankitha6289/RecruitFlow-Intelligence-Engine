import os

from app.parser.pdf_parser import PDFParser
from app.parser.docx_parser import DOCXParser


class ResumeExtractor:

    @staticmethod
    def extract(file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFParser.extract_text(file_path)

        elif extension == ".docx":
            return DOCXParser.extract_text(file_path)

        else:
            return None