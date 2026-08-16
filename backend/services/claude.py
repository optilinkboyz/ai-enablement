"""
Gemini AI service wrapper with automatic model fallback.
If the primary model is busy or unavailable, automatically tries the next one.
"""
import logging
import os
from typing import Optional

from google import genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Fallback chain — tries in order until one succeeds
MODEL_FALLBACK_CHAIN = [
    "gemini-flash-latest",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-flash-lite-latest",
]

SYSTEM_PROMPT = """You are an AI assistant for AT&S, a leading global manufacturer 
of high-end IC substrates and printed circuit boards. Help AT&S employees understand 
documents and answer questions in clear, simple language suitable for non-technical staff.
Be concise, professional, and helpful. If unsure, say so."""

# Errors that trigger a fallback (temporary/model-specific issues)
RETRYABLE_ERRORS = ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "404", "NOT_FOUND"]


def get_client() -> genai.Client:
    """Returns configured Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not found. Please set it in your .env file.")
    return genai.Client(api_key=api_key)


def _is_retryable(error_message: str) -> bool:
    """Checks if an error is temporary and worth retrying with another model."""
    return any(code in error_message for code in RETRYABLE_ERRORS)


def _generate_with_fallback(prompt: str) -> str:
    """
    Tries each model in the fallback chain until one succeeds.
    Raises RuntimeError only if ALL models fail.
    """
    client = get_client()
    last_error = None

    for model in MODEL_FALLBACK_CHAIN:
        try:
            logger.info(f"Trying model: {model}")
            response = client.models.generate_content(model=model, contents=prompt)
            logger.info(f"✅ Success with model: {model}")
            return response.text
        except Exception as e:
            error_msg = str(e)
            last_error = error_msg
            if _is_retryable(error_msg):
                logger.warning(f"⚠️ {model} unavailable ({error_msg[:80]}...) — trying next model")
                continue
            else:
                # Non-retryable error (auth, bad request) — don't try other models
                logger.error(f"Non-retryable error with {model}: {error_msg}")
                raise RuntimeError(f"AI service error: {error_msg}")

    # All models failed
    raise RuntimeError(
        f"All AI models are currently unavailable. Please try again in a moment. "
        f"Last error: {last_error[:100] if last_error else 'unknown'}"
    )


def ask_question(question: str, document_context: Optional[str] = None) -> str:
    """Sends a question to Gemini with optional document context and automatic fallback."""
    if document_context:
        prompt = f"""{SYSTEM_PROMPT}

Document content:
---
{document_context}
---

Question: {question}

Answer based on the document. If the answer is not in the document, say so clearly."""
    else:
        prompt = f"{SYSTEM_PROMPT}\n\nQuestion: {question}"

    return _generate_with_fallback(prompt)


def summarise_document(document_text: str, length: str = "medium") -> str:
    """Summarises a document at the requested length with automatic fallback."""
    length_instructions = {
        "short": "in 3-5 clear sentences",
        "medium": "in 1-2 paragraphs covering the main points",
        "detailed": "in a structured summary covering: main purpose, key points, conclusions, and action items"
    }
    instruction = length_instructions.get(length, length_instructions["medium"])

    prompt = f"""{SYSTEM_PROMPT}

Please summarise the following document {instruction}.
Write for a non-technical audience in plain language.

Document:
---
{document_text}
---

Summary:"""

    return _generate_with_fallback(prompt)
