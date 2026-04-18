from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.dashboard.models import Complaint

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Complaint).count()

    auto_routed = db.query(Complaint).filter(Complaint.route_to_human == False).count()
    human_review = db.query(Complaint).filter(Complaint.route_to_human == True).count()

    return {
        "total_complaints": total,
        "auto_routed": auto_routed,
        "human_review": human_review
    }