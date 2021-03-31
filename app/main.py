from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from .routers import sites

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    sites.router,
    prefix="/sites",
    tags=["sites"],
    responses={404: {"description": "Not found"}}
)

@app.get("/")
async def root():
    return {"message": "Welcome to my API, please go to /docs to see details."}


