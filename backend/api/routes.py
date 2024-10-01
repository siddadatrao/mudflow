from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Define the router
router = APIRouter()

# Define the request body model using Pydantic
class TextInput(BaseModel):
    text: str

# POST endpoint to process the input text
@router.post("/api/generate-post")
async def generate_post(input: TextInput):
    try:
        # Process the input text (for example, converting to uppercase)
        processed_text = f"Processed: {input.text.upper()}"

        # Return a JSON response
        return {"generated_post": processed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A simple GET endpoint for testing the API
@router.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI on Render!"}