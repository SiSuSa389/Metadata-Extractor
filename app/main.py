from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List
import sys
from loguru import logger
from .models import ExtractedMetadata, UploadResponse
from .extraction.metadata_extractor import MetadataExtractor
from .utils.file_handlers import FileHandler

# Setup logging
logger.remove()
logger.add(sys.stderr, level="INFO", format="{time} - {level} - {message}")
logger.add("logs/app.log", rotation="1 MB", level="DEBUG")

app = FastAPI(
    title="Metadata Extraction API",
    description="Extract metadata (dates, authors, key terms) from documents",
    version="1.0.0",
)

metadata_extractor = MetadataExtractor()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Metadata Extraction API")
    FileHandler.create_sample_files()


@app.get("/")
async def root():
    return {"message": "Metadata Extraction API is running!", "status": "healthy"}


@app.post("/extract", response_model=UploadResponse)
async def extract_metadata(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided"
        )

    results = []
    errors = []

    for file in files:
        try:
            if not FileHandler.validate_file_type(file.filename):
                errors.append(f"Unsupported file type: {file.filename}")
                continue

            content = await file.read()

            if not FileHandler.validate_file_size(content):
                errors.append(f"File too large: {file.filename} (max 10MB)")
                continue

            metadata = metadata_extractor.extract_metadata(file.filename, content)

            result = ExtractedMetadata(
                file_name=file.filename,
                dates=metadata["dates"],
                authors=metadata["authors"],
                key_terms=metadata["key_terms"],
                organizations=metadata.get("organizations", []),
                locations=metadata.get("locations", []),
            )
            results.append(result)
            logger.info(f"Successfully processed: {file.filename}")

        except Exception as e:
            error_msg = f"Error processing {file.filename}: {str(e)}"
            errors.append(error_msg)
            logger.error(error_msg)

    if results:
        FileHandler.save_results_to_json([r.dict() for r in results])

    message = f"Processed {len(results)} files successfully"
    if errors:
        message += f", {len(errors)} files failed"

    response = UploadResponse(message=message, results=results)

    if errors:
        return JSONResponse(
            status_code=status.HTTP_207_MULTI_STATUS,
            content={**response.dict(), "errors": errors},
        )
    return response
