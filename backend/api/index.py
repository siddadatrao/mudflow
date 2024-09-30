from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow all origins in development; Vercel will handle CORS in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class PodcastRequest(BaseModel):
    podcast_url: str

@app.post("/api/generate-post")
async def generate_post(request: PodcastRequest):
    # This is a placeholder. In a real app, you'd process the podcast and generate a post.
    return {"post": f"This is a LinkedIn post about the podcast: {request.podcast_url}"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI!"}