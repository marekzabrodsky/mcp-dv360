#!/usr/bin/env python3
"""Test MCP server startup without full stdio."""

import os
import sys
import asyncio
from pathlib import Path

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/marekzabrodsky/Downloads/dingomedia-a0dc8e320f9c.json"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dv360_mcp_server.server import DV360MCPServer

async def test_server_init():
    """Test server initialization without stdio."""
    print("🔧 Testing MCP server initialization...")
    
    try:
        # Create server instance
        dv360_server = DV360MCPServer()
        server = dv360_server.get_server()
        
        print(f"✅ Server created: {server.name}")
        
        # Test capabilities
        from mcp.server import NotificationOptions
        capabilities = server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={}
        )
        
        print(f"✅ Resources: {capabilities.resources is not None}")
        print(f"✅ Tools: {capabilities.tools is not None}")
        
        # Test config
        config = dv360_server.config
        print(f"✅ Config valid: {config.validate()}")
        
        print("🎉 Server initialization successful!")
        print("📝 The issue may be with stdio communication, not server logic")
        
        return True
        
    except Exception as e:
        print(f"❌ Server initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_server_init())
    sys.exit(0 if result else 1)