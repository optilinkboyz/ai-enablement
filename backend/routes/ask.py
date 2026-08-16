"""
Ask route.
Handles natural language questions with optional document context.
Delegates AI processing to the Claude service.
"""
import logging

from fastapi import APIRouter, HTTPException

from models.schemas import AskRequest, AskResponse, ErrorResponse
from services.claude import ask_question

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ask", tags=["Q&A"])


@router.post(
    "",
    response_model=AskResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Ask the AI a question",
    description="Ask a question with or without document context. If document context is provided, the answer is grounded in the document."
)
async def ask(request: AskRequest):
    """
    Accepts a question and optional document context.
    Returns a plain-language AI answer suitable for non-technical users.
    """
    logger.info(
        f"Question received: '{request.question[:60]}...' | "
        f"Has context: {bool(request.document_context)}"
    )

    # Validate question is not empty after stripping
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        answer = ask_question(
            question=request.question.strip(),
            document_context=request.document_context
        )
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /ask: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    logger.info(f"Answer generated: {len(answer)} characters")

    return AskResponse(
        success=True,
        question=request.question,
        answer=answer,
        has_document_context=bool(request.document_context),
        message="Answer generated successfully."
    )
