from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.auth.schemas import LoginRequest, LoginResponse, UserResponse
from src.auth.models import User
from src.auth.utils import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Mock auto-registration for MVP purposes, since no register API is defined yet
        from src.auth.utils import get_password_hash
        new_user = User(
            email=request.email,
            hashed_password=get_password_hash(request.password),
            role=request.role,
            name=request.email.split("@")[0].capitalize()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user
    else:
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
            name=user.name or user.email.split("@")[0].capitalize()
        )
    )
