from __future__ import annotations

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat_history import ChatHistory

OPENAI_URL = "https://api.openai.com/v1/responses"

SYSTEM_INSTRUCTIONS = """
You are CyberShield AI, a defensive cybersecurity assistant.

Your role:
- SOC analysis
- incident response
- threat detection
- vulnerability explanation
- secure configuration
- defensive remediation
- log analysis
- CVE explanation

Rules:
- Prefer defensive and authorized security guidance.
- Do not claim that a scan, IOC lookup, CVE result, or system action was performed unless actual data was supplied.
- Clearly distinguish facts from assumptions.
- Do not fabricate indicators, scores, CVEs, logs, or tool results.
- If information is missing, say what is missing.
"""

def ask_ai(
    db: Session,
    user_id: int,
    message: str,
) -> dict:
    api_key = settings.OPENAI_API_KEY

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI provider is not configured. Set OPENAI_API_KEY.",
        )

    payload = {
        "model": settings.OPENAI_MODEL,
        "instructions": SYSTEM_INSTRUCTIONS,
        "input": message.strip(),
        "max_output_tokens": settings.OPENAI_MAX_OUTPUT_TOKENS,
        "store": False,
    }

    try:
        response = requests.post(
            OPENAI_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=settings.OPENAI_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="AI provider is unreachable.",
        ) from exc

    if response.status_code in (401, 403):
        raise HTTPException(
            status_code=502,
            detail="AI provider rejected the configured API key.",
        )

    if response.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="AI provider rate limit reached.",
        )

    if not response.ok:
        raise HTTPException(
            status_code=502,
            detail=f"AI provider returned HTTP {response.status_code}.",
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI provider returned invalid JSON.",
        ) from exc

    answer = data.get("output_text")

    if not answer:
        # Defensive parser for response objects where output_text is not
        # directly exposed.
        chunks = []

        for item in data.get("output", []) or []:
            for content in item.get("content", []) or []:
                text = content.get("text")
                if text:
                    chunks.append(str(text))

        answer = "\n".join(chunks).strip()

    if not answer:
        raise HTTPException(
            status_code=502,
            detail="AI provider returned an empty response.",
        )

    answer = answer[:2000]

    history = ChatHistory(
        user_id=user_id,
        question=message.strip()[:1000],
        response=answer,
    )

    db.add(history)
    db.commit()

    return {
        "answer": answer,
        "provider": "OpenAI",
        "model": settings.OPENAI_MODEL,
    }
