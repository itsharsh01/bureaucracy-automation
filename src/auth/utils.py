import base64
import json
import hmac
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = "super-secret-key-for-development-mock"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode.update({"exp": int(expire.timestamp())})

    def base64url_encode(payload):
        b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode('utf-8')).decode('utf-8')
        return b64.rstrip('=')
    
    encoded_header = base64url_encode(header)
    encoded_payload = base64url_encode(to_encode)
    
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        f"{encoded_header}.{encoded_payload}".encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Mock verification for MVP without passlib."""
    return plain_password == hashed_password or plain_password + "_hashed" == hashed_password

def get_password_hash(password: str) -> str:
    """Mock hashing for MVP without passlib."""
    return password + "_hashed"
