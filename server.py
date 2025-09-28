#!/usr/bin/env python
import uvicorn
from src.jurisai.api import app

if __name__ == "__main__":
    uvicorn.run(
        "src.jurisai.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )