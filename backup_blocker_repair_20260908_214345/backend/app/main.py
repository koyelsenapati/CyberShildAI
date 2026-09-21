from fastapi import FastAPI

from app.api.alert import router as alert_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.file_integrity import router as file_integrity_router
from app.api.master_scan import router as master_scan_router
from app.api.network_monitor import router as network_monitor_router
from app.api.network_scan import router as network_scan_router
from app.api.phishing import router as phishing_router
from app.api.reports import router as reports_router
from app.api.scan import router as scan_router
from app.api.users import router as user_router
from app.api.vulnerability_scan import router as vulnerability_router
from app.api.web_scan import router as web_scan_router
from app.core.exceptions.handlers import register_exception_handlers
from app.core.middleware.logging import LoggingMiddleware
from app.core.middleware.security import SecurityHeadersMiddleware

app = FastAPI(
    title="CyberShield AI",
    description="Advanced Defensive Cybersecurity Platform",
    version="1.0.0",
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(dashboard_router)
app.include_router(web_scan_router)
app.include_router(network_scan_router)
app.include_router(network_monitor_router)
app.include_router(phishing_router)
app.include_router(vulnerability_router)
app.include_router(file_integrity_router)
app.include_router(reports_router)
app.include_router(alert_router)
app.include_router(scan_router)
app.include_router(master_scan_router)

@app.get("/")
def root():
    return {
        "application": "CyberShield AI",
        "version": "1.0.0",
        "status": "Running",
    }

@app.get("/health")
def health():
    return {"status": "Healthy"}
