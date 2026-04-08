from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.comment import CommentCreate, CommentResponse
from app.models.comment import Comment
from app.models.issue import Issue
from app.models.project import Project
from app.models.user import User
from app.db.session import getdb
from app.core.security import get_current_user

router = APIRouter(prefix="/comments")


# 🔥 ADD COMMENT
@router.post("/{issue_id}")
def add_comment(
    issue_id: int,
    comment: CommentCreate,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Check project ownership
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_comment = Comment(
        issue_id=issue_id,
        author_id=current_user.id,
        body=comment.body
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"message": "Comment added"}


# 🔥 GET COMMENTS
@router.get("/{issue_id}", response_model=List[CommentResponse])
def get_comments(
    issue_id: int,
    db: Session = Depends(getdb),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    project = db.query(Project).filter(Project.id == issue.project_id).first()

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    comments = db.query(Comment).filter(Comment.issue_id == issue_id).all()

    return comments