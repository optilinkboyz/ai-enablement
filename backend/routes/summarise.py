"""
Summarise route.
Handles document summarisation at different detail levels.
Delegates AI processing to the Claude service.
"""
import logging

from fastapi import APIRouter, HTTPException

from models.schemas import ErrorResponse, SummariseRequest, SummariseResponse
from services.claude import summarise_document

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/summarise", tags=["Summarisation"])

VALID_LENGTHS = {"short", "medium", "detailed"}


@router.post(
    "",
    response_model=SummariseResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Summarise a document",
    description="Generates a plain-language summary of a document at short, medium, or detailed length."
)
async def summarise(request: SummariseRequest):
    """
    Accepts document text and a desired summary length.
    Returns a plain-language summary suitable for non-technical users.
    """
    logger.info(
        f"Summarise request: {len(request.document_text)} chars | "
        f"Length: {request.summary_length}"
    )

    # Validate summary length
    if request.summary_length not in VALID_LENGTHS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid summary_length. Choose from: {', '.join(VALID_LENGTHS)}"
        )

    # Validate document text
    if not request.document_text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")

    try:
        summary = summarise_document(
            document_text=request.document_text.strip(),
            length=request.summary_length
        )
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /summarise: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    logger.info(f"Summary generated: {len(summary)} characters")

    return SummariseResponse(
        success=True,
        summary=summary,
        original_length=len(request.document_text),
        summary_length=len(summary),
        message="Summary generated successfully."
    )
