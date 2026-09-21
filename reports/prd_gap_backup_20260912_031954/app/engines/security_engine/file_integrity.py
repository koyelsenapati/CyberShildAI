"""
CyberShield AI
File Integrity Checker Engine

Calculates SHA-256 hashes for files.
"""

import hashlib
import os

def calculate_hash(file_path: str) -> dict:
    """
    Calculate SHA-256 hash for a file.
    """

    if not file_path or not file_path.strip():
        raise ValueError("File path cannot be empty.")

    file_path = os.path.abspath(file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            sha256.update(chunk)

    return {
        "file": file_path,
        "hash": sha256.hexdigest(),
        "algorithm": "SHA256",
        "status": "Success",
        "size": os.path.getsize(file_path),
    }

def check_file_exists(file_path: str) -> bool:
    """
    Check whether a file exists.
    """

    if not file_path:
        return False

    return os.path.isfile(
        os.path.abspath(file_path)
    )
