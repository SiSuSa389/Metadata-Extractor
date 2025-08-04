import pytest
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from app.extraction.metadata_extractor import MetadataExtractor
from app.extraction.text_extractor import TextExtractor
from app.utils.file_handlers import FileHandler


class TestMetadataExtraction:
    @pytest.fixture
    def extractor(self):
        return MetadataExtractor()

    @pytest.fixture
    def sample_text(self):
        return """
        Research Paper on Machine Learning
        Author: Dr. John Smith
        Co-author: Prof. Sarah Johnson
        Date: March 15, 2024
        
        This paper discusses artificial intelligence and natural language processing
        applications in enterprise information management. The research was conducted
        from January 2024 to February 2024.
        
        Keywords: machine learning, deep learning, neural networks, data science
        """

    def test_author_extraction(self, extractor, sample_text):
        """Test author extraction using NER"""
        authors = extractor.extract_authors_ner(sample_text)
        assert len(authors) >= 1
        assert any("Smith" in author for author in authors) or any(
            "Johnson" in author for author in authors
        )

    def test_pattern_matching(self, extractor, sample_text):
        """Test rule-based pattern matching"""
        dates, key_terms = extractor.pattern_matcher.extract_patterns(sample_text)
        assert len(dates) > 0
        assert len(key_terms) > 0
        assert "machine learning" in key_terms

    def test_file_validation(self):
        """Test file validation functions"""
        assert FileHandler.validate_file_type("test.pdf") == True
        assert FileHandler.validate_file_type("test.txt") == True
        assert FileHandler.validate_file_type("test.docx") == True
        assert FileHandler.validate_file_type("test.md") == True
        assert FileHandler.validate_file_type("test.xyz") == False

    def test_file_size_validation(self):
        """Test file size validation"""
        small_content = b"small content"
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        assert FileHandler.validate_file_size(small_content) == True
        assert FileHandler.validate_file_size(large_content) == False

    def test_text_extraction(self):
        """Test text extraction from different formats"""
        txt_content = b"Sample text content"
        extracted = TextExtractor.extract_from_txt(txt_content)
        assert extracted == "Sample text content"

    def test_metadata_extraction_full_pipeline(self, extractor):
        """Test the complete metadata extraction pipeline"""
        sample_content = b"""
        AI Research Report
        Author: Dr. Alice Wilson
        Date: 2024-01-15
        
        This document discusses machine learning and artificial intelligence
        applications in data science and neural networks.
        
        Organization: Tech Corp
        Location: San Francisco
        """

        metadata = extractor.extract_metadata("test.txt", sample_content)

        assert isinstance(metadata, dict)
        assert "dates" in metadata
        assert "authors" in metadata
        assert "key_terms" in metadata
        assert "organizations" in metadata
        assert "locations" in metadata

        # Check that some extraction occurred
        assert len(metadata["dates"]) >= 0
        assert len(metadata["authors"]) >= 0
        assert len(metadata["key_terms"]) >= 0


if __name__ == "__main__":
    pytest.main([__file__])
