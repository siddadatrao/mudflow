from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PodcastRequest(BaseModel):
    podcast_url: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Podcast RAG API"}

@app.post("/api/generate-post")
async def generate_post(request: PodcastRequest):
    # This is a placeholder. In a real app, you'd process the podcast and generate a post.
    return {"post": f"This is a LinkedIn post about the podcast: {request.podcast_url}"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}