"""
Upload route.
Handles document upload, validation, and text extraction.
Returns extracted text to the frontend for use in Q&A and summarisation.
"""
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from models.schemas import ErrorResponse, UploadResponse
from services.extractor import SUPPORTED_TYPES, extract_text, validate_file

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["Document Upload"])


@router.post(
    "",
    response_model=UploadResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Upload a document",
    description="Upload a PDF, DOCX, or TXT file. Returns the extracted text for use in Q&A and summarisation."
)
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts a document upload, validates it, extracts text, and returns it.
    The extracted text is stored client-side and sent with subsequent /ask or /summarise requests.
    """
    logger.info(f"Received upload: {file.filename} ({file.content_type})")

    # Read file bytes
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read file: {str(e)}")

    # Validate file
    is_valid, error_msg = validate_file(
        filename=file.filename,
        content_type=file.content_type,
        file_size=len(file_bytes)
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    # Extract text
    try:
        extracted_text = extract_text(file_bytes, file.content_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to extract text from document.")

    file_type = SUPPORTED_TYPES.get(file.content_type, "unknown")

    logger.info(f"Successfully extracted {len(extracted_text)} characters from {file.filename}")

    return UploadResponse(
        success=True,
        filename=file.filename,
        file_type=file_type,
        character_count=len(extracted_text),
        extracted_text=extracted_text,
        message=f"Document uploaded successfully. Extracted {len(extracted_text):,} characters."
    )
