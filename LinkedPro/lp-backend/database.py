from enum import Enum
from sqlalchemy import create_engine, Column, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import Depends

DATABASE_URL = "sqlite:///./linkedpro.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserType(Enum):
    ProfileOwner = 'PO'
    CredentialIssuer = 'CI'
    Reviewer = 'R'

class User(Base):
    __abstract__ = True
    identifier = Column(String, primary_key=True)
    hashed_password = Column(String)

class ProfileOwner(User):
    __tablename__ = 'ProfileOwner'
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    address = Column(String)

class CredentialIssuer(User):
    __tablename__ = 'CredentialIssuer'
    title = Column(String)
    type = Column(String)
    address = Column(String)
    validated = Column(Boolean)

class Reviewer(User):
    __tablename__ = 'Reviewer'
    title = Column(String)
    type = Column(String)
    address = Column(String)
    validated = Column(Boolean)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def query_user(identifier: str, user_type: UserType):
    db = SessionLocal()
    user = None
    if user_type is UserType.ProfileOwner:
        user = db.query(ProfileOwner).filter(ProfileOwner.identifier == identifier).first()
    elif user_type is UserType.CredentialIssuer:
        user = db.query(CredentialIssuer).filter(CredentialIssuer.identifier == identifier).first()
    elif user_type is UserType.Reviewer:
        user = db.query(Reviewer).filter(Reviewer.identifier == identifier).first()
    db.close()
    return user

