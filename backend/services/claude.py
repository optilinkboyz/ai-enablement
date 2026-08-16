"""
Claude API service wrapper.
All AI interactions go through this service.
Follows Single Responsibility Principle — only handles Claude API calls.
"""
import logging
import os
from typing import Optional

import anthropic
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Claude model to use
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024

# System prompt — defines AT&S assistant persona
SYSTEM_PROMPT = """You are an AI assistant for AT&S, a leading global manufacturer 
of high-end IC substrates and printed circuit boards. Your role is to help AT&S 
employees — including those without technical backgrounds — understand documents, 
answer questions, and make sense of complex information.

Guidelines:
- Always respond in clear, simple language that non-technical employees can understand
- Avoid jargon unless you explain it
- Be concise but complete
- If asked something outside the provided document context, say so clearly
- Be professional and helpful at all times
- If you are unsure, say so rather than guessing"""


def get_client() -> anthropic.Anthropic:
    """
    Returns an authenticated Anthropic client.
    Raises a clear error if API key is missing.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not found. Please set it in your .env file."
        )
    return anthropic.Anthropic(api_key=api_key)


def ask_question(question: str, document_context: Optional[str] = None) -> str:
    """
    Sends a question to Claude, optionally with document context.
    Returns the AI response as a string.
    """
    client = get_client()

    # Build user message
    if document_context:
        user_message = f"""I have uploaded a document. Here is its content:

---DOCUMENT START---
{document_context}
---DOCUMENT END---

My question is: {question}

Please answer based on the document content above. If the answer is not in the 
document, say so clearly."""
    else:
        user_message = question

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text

    except anthropic.APIConnectionError:
        raise ConnectionError("Could not connect to AI service. Please check your connection.")
    except anthropic.AuthenticationError:
        raise PermissionError("Invalid API key. Please contact your IT administrator.")
    except anthropic.RateLimitError:
        raise RuntimeError("AI service is temporarily busy. Please try again in a moment.")
    except Exception as e:
        logger.error(f"Claude API error: {str(e)}")
        raise RuntimeError(f"AI service error: {str(e)}")


def summarise_document(document_text: str, length: str = "medium") -> str:
    """
    Summarises a document at the requested length.
    length: 'short' (3-5 sentences), 'medium' (1-2 paragraphs), 'detailed' (full summary)
    """
    length_instructions = {
        "short": "in 3-5 clear sentences",
        "medium": "in 1-2 paragraphs covering the main points",
        "detailed": "in a structured summary covering: main purpose, key points, conclusions, and any action items"
    }

    instruction = length_instructions.get(length, length_instructions["medium"])

    client = get_client()

    user_message = f"""Please summarise the following document {instruction}.
Write for a non-technical audience. Use plain language.

---DOCUMENT START---
{document_text}
---DOCUMENT END---

Summary:"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text

    except anthropic.APIConnectionError:
        raise ConnectionError("Could not connect to AI service. Please check your connection.")
    except anthropic.AuthenticationError:
        raise PermissionError("Invalid API key. Please contact your IT administrator.")
    except anthropic.RateLimitError:
        raise RuntimeError("AI service is temporarily busy. Please try again in a moment.")
    except Exception as e:
        logger.error(f"Claude API error: {str(e)}")
        raise RuntimeError(f"AI service error: {str(e)}")
