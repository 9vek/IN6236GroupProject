from fastapi import FastAPI, HTTPException
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, HTTPException
from typing import List
# 创建数据库连接（SQLite内存中）
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定义数据库模型
class ProfileOwner(Base):
    __tablename__ = 'profile_owners'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  # 确保name是唯一的



class ProfileReviewer(Base):
    __tablename__ = 'profile_reviewers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class CredentialsIssuer(Base):
    __tablename__ = 'credentials_issuers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, index=True)
    real_name = Column(String)
    age = Column(Integer)
    contact_number = Column(Integer)
    educational_background = Column(String)
    work_experience = Column(String)
    professional_qualifications = Column(String)
    owner_id = Column(Integer, ForeignKey('profile_owners.id'))

class ReviewProcess(Base):
    __tablename__ = 'review_processes'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    status = Column(String)
    owner_message = Column(String)
    reviewer_message = Column(String)
    owner_id = Column(Integer, ForeignKey('profile_owners.id'))
    reviewer_id = Column(Integer, ForeignKey('profile_reviewers.id'))

# 创建数据库表

Base.metadata.create_all(bind=engine)


# 创建Pydantic模型用于数据验证



class ProfileOwnerCreate(BaseModel):
    name: str


class ProfileCreate(BaseModel):
    age: int
    contact_number: int
    educational_background: str
    work_experience: str
    professional_qualifications: str
    owner_id: int
    real_name: str


class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    contact_number: Optional[int] = None
    educational_background: Optional[str] = None
    work_experience: Optional[str] = None
    professional_qualifications: Optional[str] = None
    owner_id: Optional[int] = None
    real_name: Optional[str] = None

class ProfileReviewerBase(BaseModel):
    name: str

class ProfileReviewerCreate(ProfileReviewerBase):
    pass

class ProfileReviewerUpdate(ProfileReviewerBase):
    name: Optional[str] = None

class CredentialsIssuerBase(BaseModel):
    name: str

class CredentialsIssuerCreate(CredentialsIssuerBase):
    pass

class CredentialsIssuerUpdate(CredentialsIssuerBase):
    name: Optional[str] = None

#接口

router = APIRouter()

# 依赖项定义
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ProfileOwner 路由
@router.post("/profile_owners/", response_model=ProfileOwnerCreate)
def create_profile_owner(request_body: ProfileOwnerCreate, db: Session = Depends(get_db)):
    # 检查是否已存在具有相同 name 的 ProfileOwner
    existing_owner = db.query(ProfileOwner).filter(ProfileOwner.name == request_body.name).first()
    if existing_owner:
        raise HTTPException(status_code=400, detail="A ProfileOwner with this name already exists")

    new_owner = ProfileOwner(name=request_body.name)
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner


# Profile 路由
@router.post("/profiles/", response_model=ProfileCreate)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = Profile(
        age=profile.age,
        contact_number=profile.contact_number,
        educational_background=profile.educational_background,
        work_experience=profile.work_experience,
        professional_qualifications=profile.professional_qualifications,
        owner_id=profile.owner_id,
        real_name=profile.real_name  # 使用real_name
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/profiles/{profile_id}", response_model=ProfileCreate)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
@router.get("/profiles/by_owner/{owner_id}", response_model=List[ProfileCreate])
def get_profiles_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    profiles = db.query(Profile).filter(Profile.owner_id == owner_id).all()
    if not profiles:
        raise HTTPException(status_code=404, detail=f"No profiles found for owner with ID {owner_id}")
    return profiles

@router.get("/profiles/by_owner_name/{owner_name}", response_model=List[ProfileCreate])
def get_profiles_by_owner_name(owner_name: str, db: Session = Depends(get_db)):
    # 首先，根据name查找ProfileOwner
    owner = db.query(ProfileOwner).filter(ProfileOwner.name == owner_name).first()
    if not owner:
        raise HTTPException(status_code=404, detail="ProfileOwner not found")

    # 然后，根据owner_id查找所有相关的Profile
    profiles = db.query(Profile).filter(Profile.owner_id == owner.id).all()
    return profiles


@router.put("/profiles/{profile_id}", response_model=ProfileCreate)
def update_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_data = profile.dict(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete("/profiles/{profile_id}", status_code=204)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
    return {"message": "Profile deleted successfully"}

# ProfileReviewer 路由
@router.post("/profile_reviewers/", response_model=ProfileReviewerBase)
def create_profile_reviewer(profile_reviewer: ProfileReviewerCreate, db: Session = Depends(get_db)):
    db_profile_reviewer = ProfileReviewer(name=profile_reviewer.name)
    db.add(db_profile_reviewer)
    db.commit()
    db.refresh(db_profile_reviewer)
    return db_profile_reviewer

@router.get("/profile_reviewers/{reviewer_id}", response_model=ProfileReviewerBase)
def get_profile_reviewer(reviewer_id: int, db: Session = Depends(get_db)):
    db_profile_reviewer = db.query(ProfileReviewer).filter(ProfileReviewer.id == reviewer_id).first()
    if db_profile_reviewer is None:
        raise HTTPException(status_code=404, detail="ProfileReviewer not found")
    return db_profile_reviewer

@router.put("/profile_reviewers/{reviewer_id}", response_model=ProfileReviewerBase)
def update_profile_reviewer(reviewer_id: int, reviewer: ProfileReviewerUpdate, db: Session = Depends(get_db)):
    db_reviewer = db.query(ProfileReviewer).filter(ProfileReviewer.id == reviewer_id).first()
    if db_reviewer is None:
        raise HTTPException(status_code=404, detail="ProfileReviewer not found")
    for var, value in vars(reviewer).items():
        setattr(db_reviewer, var, value) if value else None
    db.commit()
    db.refresh(db_reviewer)
    return db_reviewer

@router.delete("/profile_reviewers/{reviewer_id}", status_code=204)
def delete_profile_reviewer(reviewer_id: int, db: Session = Depends(get_db)):
    db_reviewer = db.query(ProfileReviewer).filter(ProfileReviewer.id == reviewer_id).first()
    if db_reviewer is None:
        raise HTTPException(status_code=404, detail="ProfileReviewer not found")
    db.delete(db_reviewer)
    db.commit()
    return {"message": "ProfileReviewer deleted successfully"}

# CredentialsIssuer 路由

@router.post("/credentials_issuers/", response_model=CredentialsIssuerBase)
def create_credentials_issuer(credentials_issuer: CredentialsIssuerCreate, db: Session = Depends(get_db)):
    db_credentials_issuer = CredentialsIssuer(name=credentials_issuer.name)
    db.add(db_credentials_issuer)
    db.commit()
    db.refresh(db_credentials_issuer)
    return db_credentials_issuer

@router.get("/credentials_issuers/{issuer_id}", response_model=CredentialsIssuerBase)
def get_credentials_issuer(issuer_id: int, db: Session = Depends(get_db)):
    db_credentials_issuer = db.query(CredentialsIssuer).filter(CredentialsIssuer.id == issuer_id).first()
    if db_credentials_issuer is None:
        raise HTTPException(status_code=404, detail="CredentialsIssuer not found")
    return db_credentials_issuer

@router.put("/credentials_issuers/{issuer_id}", response_model=CredentialsIssuerBase)
def update_credentials_issuer(issuer_id: int, issuer: CredentialsIssuerUpdate, db: Session = Depends(get_db)):
    db_issuer = db.query(CredentialsIssuer).filter(CredentialsIssuer.id == issuer_id).first()
    if db_issuer is None:
        raise HTTPException(status_code=404, detail="CredentialsIssuer not found")
    issuer_data = issuer.dict(exclude_unset=True)
    for key, value in issuer_data.items():
        setattr(db_issuer, key, value) if value else None
    db.commit()
    db.refresh(db_issuer)
    return db_issuer

@router.delete("/credentials_issuers/{issuer_id}", status_code=204)
def delete_credentials_issuer(issuer_id: int, db: Session = Depends(get_db)):
    db_issuer = db.query(CredentialsIssuer).filter(CredentialsIssuer.id == issuer_id).first()
    if db_issuer is None:
        raise HTTPException(status_code=404, detail="CredentialsIssuer not found")
    db.delete(db_issuer)
    db.commit()
    return {"message": "CredentialsIssuer deleted successfully"}


#app

app = FastAPI()

app.include_router(router)

