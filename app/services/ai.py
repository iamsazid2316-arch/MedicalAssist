import logging

from openai import OpenAI

from app.services.prompts import (
    MEDICAL_ASSISTANT_SYSTEM_PROMPT,
    STRUCTURED_EXTRACTION_PROMPT,
)


logger = logging.getLogger(__name__)


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

MODEL_NAME = "llama3.2:3b"


def generate_ai_response(conversation: list[dict]) -> str:
    messages = [
        {
            "role": "system",
            "content": MEDICAL_ASSISTANT_SYSTEM_PROMPT,
        }
    ]

    messages.extend(conversation)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )

        return response.choices[0].message.content

    except Exception:
        logger.exception("AI response generation failed")
        raise RuntimeError("AI service is temporarily unavailable")


def extract_case_information(conversation: list[dict]) -> str:
    messages = [
        {
            "role": "system",
            "content": STRUCTURED_EXTRACTION_PROMPT,
        }
    ]

    messages.extend(conversation)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )

        return response.choices[0].message.content

    except Exception:
        logger.exception("AI information extraction failed")
        raise RuntimeError("AI service is temporarily unavailable")


def generate_case_summary(
    conversation: list[dict],
    extracted_information: str,
) -> str:

    summary_prompt = f"""
Create a concise medical case summary for a doctor.

Use ONLY information provided in the conversation and the
structured extraction below.

Structured extraction:
{extracted_information}

Conversation:
{conversation}

The summary should include:
- Main symptoms
- Duration
- Severity
- Relevant context
- Additional symptoms
- Missing information

Do not diagnose the patient.
Do not invent information.
Clearly indicate information that is unknown or missing.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": summary_prompt,
                }
            ],
        )

        return response.choices[0].message.content

    except Exception:
        logger.exception("AI case summary generation failed")
        raise RuntimeError("AI service is temporarily unavailable")