from jose import jwt
from typing import Annotated
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2, OAuth2PasswordBearer
from pydantic import BaseModel, ValidationError
from database import query_user
from datetime import datetime, timedelta, timezone
from database import UserType

class CurrentUser(BaseModel):
    identifier: str
    type: UserType

class OAuth2Scheme(OAuth2):
    def __init__(self, tokenUrl: str, auto_error: bool = True):
        super().__init__(scheme_name="JWT", auto_error=auto_error)
        self.tokenUrl = tokenUrl

    async def __call__(self, request: Request) -> CurrentUser:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Not authenticated")
            else:
                return None
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            else:
                return None
        return self.verify_token(token)

    def verify_token(self, token: str) -> CurrentUser:
        try:
            # Decode the token using your SECRET_KEY and ALGORITHM
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Construct CurrentUser object
            user = CurrentUser(identifier=payload["identifier"], type=UserType(payload["type"]))
            return user
        except (jwt.PyJWTError, ValidationError) as e:
            raise HTTPException(status_code=403, detail="Could not validate credentials")

SECRET_KEY = "114514"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2Scheme(tokenUrl="token")



def hash_password(password: str) -> str:
    return password_context.hash(password)

def authenticate_user(identifier: str, password: str, user_type: UserType):
    user = query_user(identifier, user_type)
    if not user:
        return False
    if password_context.verify(password, user.hashed_password):
        return True
    return False

def create_access_token(identifier: str, type: UserType):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "identifier": identifier,
        "type": str(type),
        "exp": expire
    }
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    identifier = payload.get("identifier")
    user_type = payload.get("type")
    user = query_user(identifier, user_type)
    return CurrentUser()
