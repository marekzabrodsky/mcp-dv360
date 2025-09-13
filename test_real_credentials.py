#!/usr/bin/env python3
"""Test DV360 MCP Server with real credentials."""

import asyncio
import os
import sys
from pathlib import Path

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dv360_mcp_server.server import DV360MCPServer

async def test_with_credentials():
    """Test server with real credentials."""
    print("🔧 Testing DV360 MCP Server with real credentials...")
    
    try:
        # Initialize server
        dv360_server = DV360MCPServer()
        server = dv360_server.get_server()
        
        print("✅ Server initialized with credentials")
        
        # Test credentials validation
        config = dv360_server.config
        print(f"✅ Credentials type: {config.get_credentials_type()}")
        print(f"✅ Credentials valid: {config.validate()}")
        
        # Try to initialize DV360 client
        client = dv360_server.dv360_client
        print("✅ DV360 client created")
        
        # Try to get service (this will test API access)
        try:
            print("🔍 Testing API connection...")
            # This is a safe test - just initializes the service
            service = await client._get_service()
            print("✅ DV360 API service initialized successfully!")
            print("🎉 Your MCP server is ready!")
            
        except Exception as api_error:
            print(f"⚠️  API connection issue: {api_error}")
            print("📝 This might be because:")
            print("   - DV360 API not enabled in Google Cloud")
            print("   - Service account doesn't have DV360 access")
            print("   - No DV360 account associated")
            print("💡 Server will still work once APIs are enabled!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_credentials())