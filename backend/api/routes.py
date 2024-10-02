from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from .tools.get_post import get_post_call, get_post_with_provided_transcript
from .tools.get_mp3 import download_podcast, get_script, cleanup

# Define the router
router = APIRouter()

# Define the request body model using Pydantic
class TextInput(BaseModel):
    text: str
    url: str

# POST endpoint to process the input text
@router.post("/api/generate-post")
async def generate_post(input: TextInput):
    try:

        # Process the input text (for example, converting to uppercase)
        processed_text = f"Processed: {get_post_call(input.text)}"

        # Return a JSON response
        return {"generated_post": processed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/generate-post-podcast")
async def generate_post_podcast(input: TextInput):
    print(input.url)
    try:
        # Convert url of podcast to podcast text
        file_name = download_podcast(input.url, "podcast_mp3")
        script_text = get_script(filename=file_name)
        cleanup(file_name)
        print(script_text)
        # Take input text and script text to RAG pipeline
        processed_text = f"Processed: {get_post_with_provided_transcript(input.text, script_text)}"

        # Return a JSON response
        return {"generated_post": processed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A simple GET endpoint for testing the API
@router.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI on Render!"}