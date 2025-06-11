# server.py

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Run the API server"""
    # Get port from environment variable or use default
    port = int(os.getenv("API_PORT", "8000"))
    
    # Run the server
    uvicorn.run(
        "src.agentic_api.api:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

if __name__ == "__main__":
    main()