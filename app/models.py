from pydantic import BaseModel
from typing import List, Optional


class ExtractedMetadata(BaseModel):
    file_name: str
    dates: List[str]
    authors: List[str]
    key_terms: List[str]
    organizations: Optional[List[str]] = []
    locations: Optional[List[str]] = []


class UploadResponse(BaseModel):
    message: str
    results: List[ExtractedMetadata]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
