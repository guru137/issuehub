from fastapi import FastAPI
from app.models import User
from app.db.session import engine
from app.db.base import Base
from app.routes import user
from app.models import Project
from app.routes import project
from app.models import Issue
from app.routes import issue
from app.routes import comment
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()
origins = [
    "http://localhost:5173",   # React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(issue.router)



app.include_router(comment.router)
app.include_router(project.router)

@app.get("/")
def read_root():
    return {"message" : "Issue Hub is running"}
