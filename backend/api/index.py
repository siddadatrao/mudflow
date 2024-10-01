from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class PodcastRequest(BaseModel):
    podcast_url: str

@app.post("/api/generate-post")
async def generate_post(request: PodcastRequest):
   
    return {"post": f"This is a LinkedIn post about the podcast: {request.podcast_url}"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}