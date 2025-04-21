import uvicorn
from fastapi import FastAPI

from src.router import api_router

app = FastAPI(
    title="fastAPI Final Project"
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)