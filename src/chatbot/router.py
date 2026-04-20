from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.chatbot.models import Query, QueryStatus
from src.auth.models import User, UserRole
from src.auth.utils import decode_access_token
from src.db.database import get_db
from src.models.service import predict

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

DEPARTMENT_MAP = {
    "Mortgage": "Loans",
    "Consumer Loan": "Loans",
    "Student loan": "Loans",
    "Credit card": "Credit Card",
    "Credit reporting": "Credit Reporting",
    "Debt collection": "Debt Collection",
    "Bank account or service": "Banking",
    "Money transfers": "Payments",
    "Payday loan": "Payday",
    "Prepaid card": "Payments",
    "Other financial service": "Other",
}
AVAILABLE_DEPARTMENTS = set(DEPARTMENT_MAP.values())


class RaiseQueryRequest(BaseModel):
    customer_id: int | None = None
    state: str = Field(..., min_length=1, max_length=100)
    company: str = Field(..., min_length=1, max_length=200)
    query_text: str = Field(..., min_length=1)


class RaiseQueryResponse(BaseModel):
    message: str
    id: int
    customer_id: int | None = None
    state: str
    company: str
    query_text: str
    department: str
    status: QueryStatus
    date: datetime


class PredictRequest(BaseModel):
    query_text: str = Field(..., min_length=1)


class CustomerQueryItem(BaseModel):
    id: int
    customer_id: int | None = None
    state: str
    company: str
    query_text: str
    company_response: str | None = None
    department: str
    status: QueryStatus
    date: datetime


class QueryUpdateRequest(BaseModel):
    department: str


class ForwardToCompanyRequest(BaseModel):
    query_id: int
    company_name: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)


class CompanyQueryActionRequest(BaseModel):
    action: Literal["resolve", "reject"]
    company_response: str = Field(..., min_length=1)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token.") from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


@router.post("/", response_model=RaiseQueryResponse)
def raise_query(request: RaiseQueryRequest, db: Session = Depends(get_db)):
    predicted_label = str(predict(request.query_text))
    predicted_department = DEPARTMENT_MAP.get(predicted_label, "Other")

    db_query = Query(
        customer_id=request.customer_id,
        state=request.state.strip(),
        company=request.company.strip(),
        query_text=request.query_text.strip(),
        department=predicted_department,
        status=QueryStatus.PENDING,
    )
    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    return {
        "message": "Query is raised and forwarded to the respective department wait for response.",
        "id": db_query.id,
        "customer_id": db_query.customer_id,
        "state": db_query.state,
        "company": db_query.company,
        "query_text": db_query.query_text,
        "department": db_query.department,
        "status": db_query.status,
        "date": db_query.created_at,
    }


@router.post("/predict")
def predict_api(request: PredictRequest):
    predicted_label = str(predict(request.query_text))
    predicted_department = DEPARTMENT_MAP.get(predicted_label, "Other")
    return {
        "query_text": request.query_text,
        "prediction": predicted_label,
        "department": predicted_department,
    }


@router.get("/customer/query")
def get_customer_queries(customer_id: int, db: Session = Depends(get_db)):
    queries = (
        db.query(Query)
        .filter(Query.customer_id == customer_id)
        .order_by(Query.created_at.desc())
        .all()
    )

    if not queries:
        return JSONResponse(
            status_code=201,
            content={"message": "No query available for this customer id."},
        )

    return {
        "customer_id": customer_id,
        "queries": [
            CustomerQueryItem(
                id=query.id,
                customer_id=query.customer_id,
                state=query.state,
                company=query.company,
                query_text=query.query_text,
                company_response=query.company_response,
                department=query.department,
                status=query.status,
                date=query.created_at,
            ).model_dump()
            for query in queries
        ],
    }


@router.get("/admin/queries")
def get_all_queries_for_admin(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admin can access all queries.")

    queries = db.query(Query).order_by(Query.created_at.desc()).all()
    return {
        "queries": [
            CustomerQueryItem(
                id=query.id,
                customer_id=query.customer_id,
                state=query.state,
                company=query.company,
                query_text=query.query_text,
                company_response=query.company_response,
                department=query.department,
                status=query.status,
                date=query.created_at,
            ).model_dump()
            for query in queries
        ]
    }


@router.get("/operator/queries")
def get_queries_for_operator(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.operator:
        raise HTTPException(status_code=403, detail="Only operator can access this endpoint.")
    if not current_user.department:
        raise HTTPException(status_code=400, detail="Operator has no department assigned.")

    queries = (
        db.query(Query)
        .filter(Query.department == current_user.department)
        .order_by(Query.created_at.desc())
        .all()
    )
    return {
        "department": current_user.department,
        "queries": [
            CustomerQueryItem(
                id=query.id,
                customer_id=query.customer_id,
                state=query.state,
                company=query.company,
                query_text=query.query_text,
                company_response=query.company_response,
                department=query.department,
                status=query.status,
                date=query.created_at,
            ).model_dump()
            for query in queries
        ],
    }


@router.patch("/admin/query/{query_id}/department")
def update_query_department_by_admin(
    query_id: int,
    request: QueryUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admin can change department.")
    new_department = request.department.strip()
    if new_department not in AVAILABLE_DEPARTMENTS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid department. Allowed departments: {sorted(AVAILABLE_DEPARTMENTS)}",
        )

    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found.")

    query.department = new_department
    db.commit()
    db.refresh(query)

    return {
        "message": "Department updated successfully.",
        "query_id": query.id,
        "department": query.department,
    }


@router.post("/operator/forward")
def forward_query_to_company_dashboard(
    request: ForwardToCompanyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.operator:
        raise HTTPException(status_code=403, detail="Only operator can forward queries.")
    if not current_user.department:
        raise HTTPException(status_code=400, detail="Operator has no department assigned.")

    query = db.query(Query).filter(Query.id == request.query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found.")
    if query.department != current_user.department:
        raise HTTPException(
            status_code=403,
            detail="Operator can forward only queries from their own department.",
        )

    company_user = (
        db.query(User)
        .filter(User.role == UserRole.company, User.company_name == request.company_name.strip())
        .first()
    )
    if not company_user:
        raise HTTPException(
            status_code=404,
            detail="Company user not found for the provided company name.",
        )

    query.company = request.company_name.strip()
    db.commit()
    db.refresh(query)

    return {
        "message": "Query forwarded to company dashboard successfully.",
        "query_id": query.id,
        "operator_id": current_user.id,
        "company_user_id": company_user.id,
        "company_name": company_user.company_name,
        "forward_note": request.message.strip(),
    }


@router.patch("/company/query/{query_id}/action")
def company_action_on_query(
    query_id: int,
    request: CompanyQueryActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.company:
        raise HTTPException(
            status_code=403, detail="Only company users can respond to company queries."
        )
    if not current_user.company_name:
        raise HTTPException(status_code=400, detail="Company user has no company name assigned.")

    query = db.query(Query).filter(Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found.")
    if query.company != current_user.company_name:
        raise HTTPException(
            status_code=403,
            detail="You can only act on queries assigned to your company.",
        )

    query.company_response = request.company_response.strip()
    query.status = QueryStatus.SOLVED if request.action == "resolve" else QueryStatus.CLOSED
    db.commit()
    db.refresh(query)

    return {
        "message": "Company response submitted successfully.",
        "query_id": query.id,
        "company_name": query.company,
        "company_response": query.company_response,
        "status": query.status,
    }


@router.get("/company/queries")
def get_company_queries(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.company:
        raise HTTPException(
            status_code=403, detail="Only company users can access company queries."
        )
    if not current_user.company_name:
        raise HTTPException(status_code=400, detail="Company user has no company name assigned.")

    queries = (
        db.query(Query)
        .filter(Query.company == current_user.company_name)
        .order_by(Query.created_at.desc())
        .all()
    )

    if not queries:
        return JSONResponse(
            status_code=201,
            content={"message": "No query available for this company."},
        )

    return {
        "company_name": current_user.company_name,
        "queries": [
            CustomerQueryItem(
                id=query.id,
                customer_id=query.customer_id,
                state=query.state,
                company=query.company,
                query_text=query.query_text,
                company_response=query.company_response,
                department=query.department,
                status=query.status,
                date=query.created_at,
            ).model_dump()
            for query in queries
        ],
    }
