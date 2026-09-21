"""
CyberShield AI
URL Feature Extractor
"""

from urllib.parse import urlparse
import re

IP_PATTERN = re.compile(
    r"^(?:\d{1,3}\.){3}\d{1,3}$"
)

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "is.gd",
    "ow.ly",
    "buff.ly",
    "rebrand.ly",
    "cutt.ly"
]

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "wallet",
    "paypal",
    "signin",
    "confirm",
    "free",
    "bonus",
    "gift",
    "password"
]

def extract_url_features(url: str) -> dict:
    """
    Extract URL features for phishing detection.
    """

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.lower()

    full = url.lower()

    features = {

        "url": url,

        "length": len(url),

        "domain": domain,

        "path_length": len(path),

        "uses_https": parsed.scheme == "https",

        "contains_ip": bool(
            IP_PATTERN.match(domain)
        ),

        "contains_at": "@" in url,

        "contains_dash": "-" in domain,

        "subdomain_count": max(
            domain.count(".") - 1,
            0
        ),

        "digit_count": sum(
            c.isdigit() for c in url
        ),

        "special_char_count": sum(
            not c.isalnum()
            for c in url
        ),

        "is_shortened": any(
            short in domain
            for short in SHORTENERS
        ),

        "suspicious_words": []
    }

    for word in SUSPICIOUS_WORDS:

        if word in full:

            features["suspicious_words"].append(word)

    features["suspicious_word_count"] = len(
        features["suspicious_words"]
    )

    return features
