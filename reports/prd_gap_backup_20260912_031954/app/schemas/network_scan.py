from pydantic import BaseModel

class ServiceInfo(BaseModel):
    port: int
    protocol: str
    service: str
    product: str
    version: str
    state: str
    risk: str

class NetworkScanCreate(BaseModel):
    target: str
    scan_type: str = "Basic"

class NetworkScanResponse(BaseModel):
    id: int
    target: str
    status: str
    open_ports: int
    devices_found: int
    scan_type: str

    class Config:
        from_attributes = True

class NetworkScanDetails(BaseModel):
    devices_found: int
    open_ports: int
    services: list[ServiceInfo]
