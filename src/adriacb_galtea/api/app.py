"""FastAPI application setup."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router

app = FastAPI(
    title="AdriaCB Galtea",
    description="RAG application with FastAPI",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1") 