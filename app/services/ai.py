import logging
import os

from openai import OpenAI

from app.services.prompts import (
    MEDICAL_ASSISTANT_SYSTEM_PROMPT,
    STRUCTURED_EXTRACTION_PROMPT,
)


logger = logging.getLogger(__name__)


client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
    timeout=float(os.getenv("MEDICALASSIST_AI_TIMEOUT", "5")),
    max_retries=0,
)

MODEL_NAME = os.getenv("MEDICALASSIST_AI_MODEL", "llama3.2:3b")


def _offline_response(conversation: list[dict]) -> str:
    latest = next(
        (
            str(item.get("content", ""))
            for item in reversed(conversation)
            if item.get("role") == "user"
        ),
        "",
    ).lower()

    emergency_terms = (
        "difficulty breathing",
        "severe chest pain",
        "uncontrolled bleeding",
        "loss of consciousness",
        "seizure",
    )
    if any(term in latest for term in emergency_terms):
        return (
            "This may be an emergency. Contact local emergency services and a doctor "
            "immediately. Do not wait for this chat."
        )

    asked = " ".join(str(item.get("content", "")).lower() for item in conversation)
    if "how long" not in asked and not any(word in latest for word in ("day", "week", "hour")):
        return "How long have you had these symptoms?"
    if "severity" not in asked and not any(str(number) in latest for number in range(1, 11)):
        return "How severe is it on a scale from 1 to 10?"
    return (
        "Thank you. Your information has been recorded for doctor review. "
        "If your symptoms suddenly worsen, seek urgent medical help."
    )


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
        logger.warning("AI service unavailable; using safe offline assistant", exc_info=True)
        return _offline_response(conversation)


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
        logger.warning("AI extraction unavailable; using conversation transcript", exc_info=True)
        return "\n".join(
            f"{item.get('role', 'unknown')}: {item.get('content', '')}"
            for item in conversation
        )


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
        logger.warning("AI summary unavailable; using structured information", exc_info=True)
        return extracted_information.strip() or "No structured summary is available."
