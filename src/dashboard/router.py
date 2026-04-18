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

@router.get("/distribution")
def get_distribution(db: Session = Depends(get_db)):
    results = db.query(Complaint.product).all()

    distribution = {}

    for (product,) in results:
        distribution[product] = distribution.get(product, 0) + 1

    return distribution

@router.get("/recent")
def get_recent(db: Session = Depends(get_db)):
    results = db.query(Complaint).order_by(Complaint.timestamp.desc()).limit(5).all()

    data = []

    for r in results:
        data.append({
            "id": r.id,
            "complaint": r.complaint,
            "product": r.product,
            "confidence": r.confidence,
            "timestamp": r.timestamp
        })

    return data

