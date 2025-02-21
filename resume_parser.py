import fitz  # PyMuPDF
from docx import Document
from typing import Optional

class ResumeParser:
    @staticmethod
    def parse_pdf(file_content: bytes) -> Optional[str]:
        """Extract text from PDF file"""
        try:
            with fitz.open(stream=file_content, filetype="pdf") as pdf_doc:
                text = ""
                for page in pdf_doc:
                    text += page.get_text()
                return text.strip()
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            return None

    @staticmethod
    def parse_docx(file_content: bytes) -> Optional[str]:
        """Extract text from DOCX file"""
        try:
            from io import BytesIO
            doc = Document(BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error parsing DOCX: {str(e)}")
            return None

    @classmethod
    def parse_resume(cls, file_content: bytes, file_type: str) -> Optional[str]:
        """Parse resume based on file type"""
        if file_type.lower() == "pdf":
            return cls.parse_pdf(file_content)
        elif file_type.lower() == "docx":
            return cls.parse_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")