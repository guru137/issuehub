from pydantic import BaseModel, Field, ConfigDict

class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)


class CommentResponse(BaseModel):
    id: int
    issue_id: int
    author_id: int
    body: str

    model_config = ConfigDict(from_attributes=True)