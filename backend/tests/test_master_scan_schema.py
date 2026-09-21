from app.schemas.master_scan import MasterScanResponse, MasterScanHistoryResponse

def test_master_scan_response_contract():
    response = MasterScanResponse(
        scan_id=1,
        status="Completed",
        target="https://example.com",
        risk_level="Low",
        risk_breakdown={"web": "Low", "network": "Low", "vulnerability": "Low", "phishing": "Low"},
        report_id=2,
    )
    assert response.scan_id == 1
    assert response.report_id == 2

def test_master_scan_history_contract():
    response = MasterScanHistoryResponse(status="Success", count=0, scans=[])
    assert response.count == 0
