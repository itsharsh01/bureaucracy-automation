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

    # percentages
    auto_percent = (auto_routed / total * 100) if total > 0 else 0
    human_percent = (human_review / total * 100) if total > 0 else 0

    # top category
    results = db.query(Complaint.product).all()
    category_count = {}

    for (product,) in results:
        category_count[product] = category_count.get(product, 0) + 1

    top_category = max(category_count, key=category_count.get) if category_count else None

    return {
        "total_complaints": total,
        "auto_routed": auto_routed,
        "human_review": human_review,
        "auto_percent": auto_percent,
        "human_percent": human_percent,
        "top_category": top_category
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

@router.get("/manual_review")
def get_manual_review(db: Session = Depends(get_db)):
    results = db.query(Complaint).filter(Complaint.route_to_human == True).all()

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

@router.get("/complaint/{complaint_id}")
def get_complaint_detail(complaint_id: int, db: Session = Depends(get_db)):
    result = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if not result:
        return {"error": "Complaint not found"}

    return {
        "id": result.id,
        "complaint": result.complaint,
        "product": result.product,
        "dispute_probability": result.dispute_probability,
        "confidence": result.confidence,
        "route_to_human": result.route_to_human,
        "timestamp": result.timestamp
    }


@router.get("/queue")
def get_queue(db: Session = Depends(get_db)):
    results = db.query(Complaint).order_by(Complaint.timestamp.desc()).all()

    data = []

    for r in results:
        data.append({
            "id": r.id,
            "complaint": r.complaint[:100],  # preview
            "product": r.product,
            "confidence": r.confidence,
            "status": "Auto" if not r.route_to_human else "Needs Review",
            "timestamp": r.timestamp
        })

    return data

from pydantic import BaseModel

class UpdateComplaintRequest(BaseModel):
    product: str | None = None
    route_to_human: bool | None = None


@router.put("/complaint/{complaint_id}")
def update_complaint(complaint_id: int, data: UpdateComplaintRequest, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if not complaint:
        return {"error": "Complaint not found"}

    if data.product is not None:
        complaint.product = data.product

    if data.route_to_human is not None:
        complaint.route_to_human = data.route_to_human

    db.commit()
    db.refresh(complaint)

    return {"message": "Complaint updated successfully"}


@router.get("/routing")
def get_routing():
    routing_map = {
        "Credit card": "Payments Team",
        "Mortgage": "Loans Team",
        "Bank account": "Banking Team",
        "Debt collection": "Recovery Team",
        "Student loan": "Education Loans Team"
    }

    return routing_map