from pydantic import BaseModel, Field, ConfigDict

class IssueCreate(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)
    project_id: int
    priority: str = "medium"




class IssueResponse(BaseModel):
    id: int
    title: str
    description: str
    project_id: int
    created_by: int
    assigned_to: int | None
    status: str
    priority: str

    model_config = ConfigDict(from_attributes=True)