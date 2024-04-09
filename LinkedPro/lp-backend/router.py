from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import User, ProfileOwner, UserType, get_db
from security import CurrentUser, authenticate_user, create_access_token, hash_password, get_current_user
from pydantic import BaseModel

"""
Profile Owner
"""
class ProfileOwnerRequest(BaseModel):
    identifier: str
    password: str

class ProfileOwnerResponse(BaseModel):
    identifier: str

class TokenRequest(BaseModel):
    identifier: str
    password: str
    user_type: UserType

class Token(BaseModel):
    identifier: str
    token: str
    type: str

router = APIRouter()

@router.post("/profile-owners/", response_model=ProfileOwnerResponse)
def create_profile_owner(profile_owner: ProfileOwnerRequest, db: Session = Depends(get_db)):
    if db.query(ProfileOwner).filter(ProfileOwner.identifier == profile_owner.identifier).first():
        raise HTTPException(status_code=400, detail="A ProfileOwner with this name already exists")
    profile_owner = ProfileOwner(
        identifier=profile_owner.identifier, 
        hashed_password=hash_password(profile_owner.password)
    )
    db.add(profile_owner)
    db.commit()
    db.refresh(profile_owner)
    return ProfileOwnerResponse(
        identifier=profile_owner.identifier
    )

@router.post("/token", response_model=Token)
def access_token(user: TokenRequest):
    if not authenticate_user(user.identifier, user.password, user.user_type):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    access_token = create_access_token(user.identifier, user.user_type)
    return Token(
        identifier=user.identifier, 
        token=access_token, 
        type="bearer"
    )

@router.get("/profile-owners/me")
def read_profile_owner(user: Annotated[CurrentUser, Depends(get_current_user)]):
    if user.type is UserType.ProfileOwner:
        return {'success': '111', 'identifier': user.identifier}