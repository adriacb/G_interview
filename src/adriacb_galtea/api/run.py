"""Script to run the FastAPI server."""
import uvicorn

from .app import app

if __name__ == "__main__":
    uvicorn.run(
        "adriacb_galtea.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 