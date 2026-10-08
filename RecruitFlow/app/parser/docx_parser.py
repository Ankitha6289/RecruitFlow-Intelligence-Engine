from docx import Document


class DOCXParser:

    @staticmethod
    def extract_text(file_path):

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text