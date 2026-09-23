from datetime import datetime, timedelta, timezone
from uuid import UUID
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .config import get_settings
from .db import get_db
from .models import User

_hasher = PasswordHasher()
_bearer = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str: return _hasher.hash(password)
def verify_password(password: str, password_hash: str) -> bool:
    try: return _hasher.verify(password_hash, password)
    except VerificationError: return False

def create_token(user: User) -> str:
    settings=get_settings(); now=datetime.now(timezone.utc)
    return jwt.encode({'sub':str(user.id),'role':user.role,'iat':now,'exp':now+timedelta(minutes=settings.jwt_exp_minutes)}, settings.jwt_secret, algorithm='HS256')

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer), db: Session = Depends(get_db)) -> User:
    if not credentials: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication required')
    try: payload=jwt.decode(credentials.credentials, get_settings().jwt_secret, algorithms=['HS256']); user_id=UUID(payload['sub'])
    except (jwt.InvalidTokenError, KeyError, ValueError): raise HTTPException(status_code=401, detail='Invalid access token')
    user=db.get(User,user_id)
    if not user or not user.is_active: raise HTTPException(status_code=401, detail='User is inactive')
    return user

def admin_user(user: User = Depends(current_user)) -> User:
    if user.role != 'ADMIN': raise HTTPException(status_code=403, detail='Admin role required')
    return user
