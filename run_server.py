#!/usr/bin/env python3
"""Direct executable for DV360 MCP Server."""

import sys
import os
from pathlib import Path

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import and run the server
from dv360_mcp_server.server_minimal import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())