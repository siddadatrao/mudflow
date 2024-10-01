from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import routes
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://medflow-frontend.onrender.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8000)),
    )