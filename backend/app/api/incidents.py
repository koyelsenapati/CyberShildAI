from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.database.database import get_db
from app.models.incident import Incident
from app.schemas.prd_features import IncidentCreateRequest, IncidentUpdateRequest, IncidentResponse

router = APIRouter(prefix="/incidents", tags=["Incident Response"])

def _owned(db: Session, incident_id: int, user_id: int):
    return db.query(Incident).filter(Incident.id == incident_id, Incident.user_id == user_id).first()

@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    incident = Incident(user_id=current_user.id, **payload.model_dump())
    db.add(incident); db.commit(); db.refresh(incident)
    return incident

@router.get("/", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Incident).filter(Incident.user_id == current_user.id).order_by(Incident.created_at.desc()).all()

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    incident = _owned(db, incident_id, current_user.id)
    if not incident: raise HTTPException(status_code=404, detail="Incident not found.")
    return incident

@router.patch("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, payload: IncidentUpdateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    incident = _owned(db, incident_id, current_user.id)
    if not incident: raise HTTPException(status_code=404, detail="Incident not found.")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(incident, key, value)
    db.commit(); db.refresh(incident)
    return incident
