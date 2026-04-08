import email

from fastapi import APIRouter,Depends, HTTPException
from app.core.security import hash_password
from sqlalchemy.orm import Session
from app.db.session import getdb
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.core.security import verify_password, create_access_token
from app.core.security import get_current_user




router=APIRouter()

@router.post("/signup")
def signup(user :UserCreate,db :Session = Depends(getdb)) :

    existing_user =db.query(User).filter(User.email==user.email).first()
    if existing_user :
        raise  HTTPException(status_code=400,detail="email already registered")
    new_user=User(
        name =user.name,
        email =user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"messages" :"User Created Successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(getdb)):
    
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentails")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentails")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email
    }
