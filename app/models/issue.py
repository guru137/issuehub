from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="open", nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    priority = Column(String, default="medium", nullable=False)

    project = relationship("Project")
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])