
from typing import List
from sqlalchemy import asc, desc

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.issue import IssueCreate, IssueResponse
from app.models.issue import Issue
from app.models.project import Project
from app.models.user import User
from app.db.session import getdb
from app.core.security import get_current_user



router = APIRouter(prefix="/issues")


#  CREATE ISSUE
@router.post("/")
def create_issue(
    issue: IssueCreate,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    # Check project exists
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check ownership
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_issue = Issue(
      title=issue.title,
      description=issue.description,
      project_id=issue.project_id,
      created_by=current_user.id,
      priority=issue.priority
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return {"message": "Issue created"}



@router.get("/{project_id}", response_model=List[IssueResponse])
def get_issues_by_project(
    project_id: int,
    q: str | None = None,
    status: str | None = None,
    assigned_to: int | None = None,
    sort: str | None = None,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    query = db.query(Issue).filter(Issue.project_id == project_id)

    # 🔍 SEARCH
    if q:
        query = query.filter(Issue.title.ilike(f"%{q}%"))

    # 🔍 FILTERS
    if status:
        query = query.filter(Issue.status == status)

    if assigned_to:
        query = query.filter(Issue.assigned_to == assigned_to)

    # 🔽 SORTING
    if sort == "created_at":
        query = query.order_by(desc(Issue.id))  # newest first

    elif sort == "priority":
        query = query.order_by(desc(Issue.priority))

    elif sort == "status":
        query = query.order_by(asc(Issue.status))

    issues = query.all()

    return issues

#  ASSIGN ISSUE
@router.put("/assign/{issue_id}/{user_id}")
def assign_issue(
    issue_id: int,
    user_id: int,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Check user exists
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check ownership via project
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    issue.assigned_to = user_id

    db.commit()
    db.refresh(issue)

    return {"message": "Issue assigned"}


#  UPDATE ISSUE STATUS
@router.put("/status/{issue_id}")
def update_issue_status(
    issue_id: int,
    status: str,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Check ownership via project
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Validate status
    valid_status = ["open", "in_progress", "closed"]
    if status not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status")

    issue.status = status

    db.commit()
    db.refresh(issue)

    return {"message": "Status updated"}


@router.patch("/{issue_id}")
def update_issue(
    issue_id: int,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    assigned_to: int | None = None,
    priority :str | None =None,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    #  Check ownership
    project = db.query(Project).filter(Project.id == issue.project_id).first()
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 🧠 Update fields only if provided
    if title:
        issue.title = title

    if description:
        issue.description = description

    if status:
        valid_status = ["open", "in_progress", "closed"]
        if status not in valid_status:
            raise HTTPException(status_code=400, detail="Invalid status")
        issue.status = status

    if assigned_to:
        user = db.query(User).filter(User.id == assigned_to).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        issue.assigned_to = assigned_to

    if priority:
      valid_priority = ["low", "medium", "high", "critical"]
      if priority not in valid_priority:
        raise HTTPException(status_code=400, detail="Invalid priority")
      issue.priority = priority

    db.commit()
    db.refresh(issue)

    return {"message": "Issue updated"}


@router.delete("/{issue_id}")
def delete_issue(
    issue_id: int,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # 🔐 Check ownership
    project = db.query(Project).filter(Project.id == issue.project_id).first()
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(issue)
    db.commit()

    return {"message": "Issue deleted"}


@router.get("/single/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, db: Session = Depends(getdb)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    return issue