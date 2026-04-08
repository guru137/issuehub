from pydantic import BaseModel, Field, ConfigDict

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=5)



from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)