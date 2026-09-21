import json

from sqlalchemy.orm import Session

from app.crud.web_scan import create_scan
from app.engines.security_engine.web_scan import scan_website

def scan_url(
    db: Session,
    url: str,
    user_id: int,
) -> dict:
    """
    Execute WebScan, persist the canonical result,
    and return the same contract used by the API.
    """

    result = scan_website(url)

    data = {
        "user_id": user_id,
        "url": url,
        "status": result.get("status"),
        "response_time": result.get("response_time"),
        "risk_level": result.get("risk_level"),
        "ssl_status": json.dumps(
            result.get("ssl_status"),
            default=str,
        ),
        "result": json.dumps(
            result,
            default=str,
        ),
    }

    persisted = create_scan(db, data)

    return {
        "id": persisted.id,
        "user_id": persisted.user_id,
        "url": persisted.url,
        "status": result.get("status"),
        "domain": result.get("domain"),
        "response_time": result.get("response_time"),
        "ssl_status": result.get("ssl_status"),
        "security_headers": result.get("security_headers"),
        "cookies": result.get("cookies"),
        "html": result.get("html"),
        "robots": result.get("robots"),
        "sql_injection": result.get("sql_injection"),
        "xss": result.get("xss"),
        "csrf": result.get("csrf"),
        "risk_level": result.get("risk_level"),
        "result": result,
        "report_id": persisted.id,
    }
