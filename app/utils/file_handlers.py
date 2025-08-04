import os
import json
from typing import List, Dict
from pathlib import Path
from loguru import logger


class FileHandler:
    @staticmethod
    def validate_file_type(filename: str) -> bool:
        supported_exts = {".pdf", ".docx", ".txt", ".md"}
        ext = Path(filename).suffix.lower()
        return ext in supported_exts

    @staticmethod
    def validate_file_size(content: bytes, max_size_mb: int = 10) -> bool:
        size_mb = len(content) / (1024 * 1024)
        return size_mb <= max_size_mb

    @staticmethod
    def save_results_to_json(
        results: List[Dict], output_path: str = "data/output/results.json"
    ):
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    @staticmethod
    def create_sample_files():
        sample_dir = Path("data/sample_documents")
        sample_dir.mkdir(parents=True, exist_ok=True)

        sample_content = """
Artificial Intelligence and Machine Learning Research Report

Author: Dr. John Smith
Co-Author: Prof. Sarah Johnson
Date: March 15, 2024

Abstract:
This research paper explores applications of natural language processing,
deep learning techniques, and neural networks.

Keywords: machine learning, artificial intelligence, natural language processing,
document classification, enterprise information management, neural networks

Organization: OpenText Corporation
Location: Waterloo, Canada
"""

        with open(sample_dir / "sample_research.txt", "w") as f:
            f.write(sample_content)
        logger.info(f"Sample files created in {sample_dir}")
