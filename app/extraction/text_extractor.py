import io
from pdfminer.high_level import extract_text
from docx import Document
from loguru import logger


class TextExtractor:
    @staticmethod
    def extract_from_pdf(content: bytes) -> str:
        try:
            return extract_text(io.BytesIO(content))
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def extract_from_docx(content: bytes) -> str:
        try:
            doc = Document(io.BytesIO(content))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs)
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

    @staticmethod
    def extract_from_txt(content: bytes) -> str:
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return content.decode("latin-1")
            except Exception as e:
                logger.error(f"TXT extraction error: {e}")
                raise ValueError(f"Failed to extract text from TXT: {str(e)}")

    @classmethod
    def extract_text(cls, filename: str, content: bytes) -> str:
        fname_lower = filename.lower()
        if fname_lower.endswith(".pdf"):
            return cls.extract_from_pdf(content)
        elif fname_lower.endswith(".docx"):
            return cls.extract_from_docx(content)
        elif fname_lower.endswith((".txt", ".md")):
            return cls.extract_from_txt(content)
        else:
            raise ValueError(f"Unsupported file type: {filename}")
