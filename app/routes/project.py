from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate
from app.models.project import Project
from app.db.session import getdb
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.project import ProjectResponse


router = APIRouter(prefix="/projects")

@router.post("/")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    

    existing = db.query(Project).filter(
    Project.name == project.name,
    Project.owner_id == current_user.id).first()

    if existing:
         raise HTTPException(status_code=400, detail="Project already exists")
    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {"message": "Project created"}


@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects