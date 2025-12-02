"""
Quick start script for PRATT application.
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Use 127.0.0.1 for local access, or 0.0.0.0 for network access
        port=8000,
        reload=True
    )

