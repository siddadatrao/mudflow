from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PodcastRequest(BaseModel):
    podcast_url: str

@app.post("/api/generate-post")
async def generate_post(request: PodcastRequest):
    return {"post": f"This is a LinkedIn post about the podcast: {request.podcast_url}"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}