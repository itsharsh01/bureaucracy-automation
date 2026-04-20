from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)
from src.auth.models import User, UserRole
from src.auth.utils import verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/api/auth", tags=["Auth"])

AVAILABLE_DEPARTMENTS = {
    "Loans",
    "Credit Card",
    "Credit Reporting",
    "Debt Collection",
    "Banking",
    "Payments",
    "Payday",
    "Other",
}


def validate_role_specific_fields(
    role: UserRole,
    department: str | None,
    company_name: str | None,
    *,
    require_operator_department: bool,
) -> None:
    if role == UserRole.operator:
        if require_operator_department and not department:
            raise HTTPException(
                status_code=400, detail="Department is required for operator role."
            )
        if department and department.strip() not in AVAILABLE_DEPARTMENTS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid operator department. Allowed departments: {sorted(AVAILABLE_DEPARTMENTS)}",
            )

    if role == UserRole.company and not company_name:
        raise HTTPException(
            status_code=400, detail="Company name is required for company role."
        )


def resolve_company_name(company_name: str | None, company: str | None) -> str | None:
    if company_name and company_name.strip():
        return company_name.strip()
    if company and company.strip():
        return company.strip()
    return None


@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    normalized_company_name = resolve_company_name(request.company_name, request.company)
    normalized_department = request.department.strip() if request.department else None
    validate_role_specific_fields(
        request.role,
        normalized_department,
        normalized_company_name,
        require_operator_department=True,
    )

    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists with this email.")
    if request.role == UserRole.operator and normalized_department:
        existing_operator_dept = (
            db.query(User)
            .filter(
                User.role == UserRole.operator,
                User.department == normalized_department,
            )
            .first()
        )
        if existing_operator_dept:
            raise HTTPException(
                status_code=409,
                detail="Operator already exists for this department.",
            )
    if request.role == UserRole.company and normalized_company_name:
        existing_company = (
            db.query(User)
            .filter(
                User.role == UserRole.company,
                User.company_name == normalized_company_name,
            )
            .first()
        )
        if existing_company:
            raise HTTPException(
                status_code=409,
                detail="Company user already exists for this company name.",
            )

    new_user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        role=request.role,
        name=(request.name or request.email.split("@")[0].capitalize()),
        department=normalized_department,
        company_name=normalized_company_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RegisterResponse(
        message="User registered successfully.",
        user=UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            role=new_user.role,
            name=new_user.name,
            department=new_user.department,
            company_name=new_user.company_name,
        ),
    )

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.role != request.role:
        raise HTTPException(status_code=403, detail="Role mismatch. User is registered with a different role.")

    token_data = {"sub": str(user.id), "role": user.role.value}
    token = create_access_token(data=token_data)

    return LoginResponse(
        token=token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            role=user.role,
            name=user.name or user.email.split("@")[0].capitalize(),
            department=user.department,
            company_name=user.company_name,
        )
    )
