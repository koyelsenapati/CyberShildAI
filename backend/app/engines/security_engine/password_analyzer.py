import math
import re

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "admin123",
    "letmein",
    "welcome",
}

def analyze_password(password: str) -> dict:
    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    length = len(password)
    lower = bool(re.search(r"[a-z]", password))
    upper = bool(re.search(r"[A-Z]", password))
    digit = bool(re.search(r"\d", password))
    special = bool(re.search(r"[^A-Za-z0-9]", password))

    pool = 0

    if lower:
        pool += 26
    if upper:
        pool += 26
    if digit:
        pool += 10
    if special:
        pool += 33

    entropy = round(length * math.log2(pool), 2) if pool else 0
    common = password.lower() in COMMON_PASSWORDS

    score = 0

    if length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    elif length >= 6:
        score += 10

    score += 15 if lower else 0
    score += 15 if upper else 0
    score += 15 if digit else 0
    score += 15 if special else 0

    if common:
        score = min(score, 20)

    if score >= 80:
        strength = "Strong"
    elif score >= 60:
        strength = "Good"
    elif score >= 40:
        strength = "Medium"
    else:
        strength = "Weak"

    suggestions = []

    if length < 12:
        suggestions.append("Use at least 12 characters.")
    if not lower:
        suggestions.append("Add lowercase letters.")
    if not upper:
        suggestions.append("Add uppercase letters.")
    if not digit:
        suggestions.append("Add numbers.")
    if not special:
        suggestions.append("Add special characters.")
    if common:
        suggestions.append("Avoid common passwords.")

    brute_force_seconds = (2 ** entropy) / 1_000_000_000 if entropy else 0

    return {
        "score": score,
        "strength": strength,
        "entropy": entropy,
        "common_password": common,
        "brute_force_seconds": brute_force_seconds,
        "suggestions": suggestions,
    }
