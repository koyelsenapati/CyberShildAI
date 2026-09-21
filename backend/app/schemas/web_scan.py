from typing import Any

from pydantic import BaseModel, ConfigDict, HttpUrl

class WebScanCreate(BaseModel):
    url: HttpUrl

class WebScanResponse(BaseModel):
    id: int | None = None
    user_id: int | None = None

    url: str
    status: str
    domain: str | None = None
    response_time: float | None = None

    ssl_status: dict[str, Any] | None = None
    security_headers: dict[str, Any] | None = None
    cookies: dict[str, Any] | None = None
    html: dict[str, Any] | None = None
    robots: dict[str, Any] | None = None
    sql_injection: dict[str, Any] | None = None
    xss: dict[str, Any] | None = None
    csrf: dict[str, Any] | None = None

    risk_level: str | None = None

    result: dict[str, Any] | None = None
    report_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
