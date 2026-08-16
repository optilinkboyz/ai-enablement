"""
Pydantic schemas for request and response models.
Defines the data contracts between frontend and backend.
"""
from pydantic import BaseModel, Field
from typing import Optional


# ── Request Models ────────────────────────────────────────────────────────────

class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="The question to ask the AI assistant"
    )
    document_context: Optional[str] = Field(
        default=None,
        description="Extracted text from an uploaded document (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the main topic of this document?",
                "document_context": "This document describes your organisation quality standards..."
            }
        }


class SummariseRequest(BaseModel):
    """Request model for the /summarise endpoint."""
    document_text: str = Field(
        ...,
        min_length=10,
        description="The full extracted text of the document to summarise"
    )
    summary_length: Optional[str] = Field(
        default="medium",
        description="Desired summary length: 'short', 'medium', or 'detailed'"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "document_text": "This report covers Q1 production results...",
                "summary_length": "medium"
            }
        }


# ── Response Models ───────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""
    status: str
    version: str
    message: str


class UploadResponse(BaseModel):
    """Response model for the /upload endpoint."""
    success: bool
    filename: str
    file_type: str
    character_count: int
    extracted_text: str
    message: str


class AskResponse(BaseModel):
    """Response model for the /ask endpoint."""
    success: bool
    question: str
    answer: str
    has_document_context: bool
    message: str


class SummariseResponse(BaseModel):
    """Response model for the /summarise endpoint."""
    success: bool
    summary: str
    original_length: int
    summary_length: int
    message: str


class ErrorResponse(BaseModel):
    """Standard error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None
