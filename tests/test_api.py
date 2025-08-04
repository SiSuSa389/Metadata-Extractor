import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
import io

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app

client = TestClient(app)


class TestAPI:
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Metadata Extraction API is running" in response.json()["message"]

    def test_detailed_health_check(self):
        """Test detailed health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_single_file_upload(self):
        """Test single file upload endpoint"""
        # Create a test file
        test_content = """
        Test Document
        Author: John Doe
        Date: 2024-01-15
        This document discusses machine learning and artificial intelligence.
        """

        files = {"file": ("test.txt", io.BytesIO(test_content.encode()), "text/plain")}
        response = client.post("/extract-single", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["file_name"] == "test.txt"
        assert isinstance(data["dates"], list)
        assert isinstance(data["authors"], list)
        assert isinstance(data["key_terms"], list)

    def test_multiple_file_upload(self):
        """Test multiple file upload endpoint"""
        # Create test files
        test_content1 = """
        Document 1
        Author: Jane Smith
        Date: 2024-02-01
        Research on neural networks and deep learning.
        """

        test_content2 = """
        Document 2
        Author: Bob Johnson  
        Date: 2024-02-02
        Analysis of machine learning algorithms.
        """

        files = [
            ("files", ("doc1.txt", io.BytesIO(test_content1.encode()), "text/plain")),
            ("files", ("doc2.txt", io.BytesIO(test_content2.encode()), "text/plain")),
        ]

        response = client.post("/extract", files=files)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "results" in data
        assert len(data["results"]) == 2

        # Check first result
        assert data["results"][0]["file_name"] == "doc1.txt"
        assert isinstance(data["results"][0]["dates"], list)
        assert isinstance(data["results"][0]["authors"], list)
        assert isinstance(data["results"][0]["key_terms"], list)

    def test_unsupported_file_type(self):
        """Test upload of unsupported file type"""
        files = {
            "file": ("test.xyz", io.BytesIO(b"content"), "application/octet-stream")
        }
        response = client.post("/extract-single", files=files)

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_empty_file_upload(self):
        """Test upload of empty file"""
        files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
        response = client.post("/extract-single", files=files)

        # Should still return 200 but with empty results
        assert response.status_code == 200
        data = response.json()
        assert data["file_name"] == "empty.txt"
        assert len(data["dates"]) == 0
        assert len(data["authors"]) == 0
        assert len(data["key_terms"]) == 0

    def test_large_file_upload(self):
        """Test upload of file that's too large"""
        # Create a large file (>10MB)
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        files = {"file": ("large.txt", io.BytesIO(large_content), "text/plain")}

        response = client.post("/extract-single", files=files)

        assert response.status_code == 413
        assert "File too large" in response.json()["detail"]

    def test_no_files_provided(self):
        """Test extract endpoint with no files"""
        response = client.post("/extract", files=[])

        assert (
            response.status_code == 422
        )  # FastAPI validation error for empty file list


if __name__ == "__main__":
    pytest.main([__file__])
