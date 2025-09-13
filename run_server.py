#!/usr/bin/env python3
"""Run the DV360 MCP Server."""

import os
import sys
from pathlib import Path

# Set credentials path - update this to your actual credentials file
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import and run the server
from dv360_mcp_server.server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())