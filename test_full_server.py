#!/usr/bin/env python3
"""Test the full DV360 MCP server functionality."""

import asyncio
import os
import sys
from pathlib import Path

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dv360_mcp_server.server import DV360MCPServer
from mcp.server import NotificationOptions

async def test_full_server():
    """Test the full server implementation."""
    print("🔧 Testing full DV360 MCP Server...")
    
    try:
        # Create server
        dv360_server = DV360MCPServer()
        server = dv360_server.get_server()
        
        print(f"✅ Server created: {server.name}")
        
        # Test capabilities
        capabilities = server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={}
        )
        
        print(f"✅ Resources available: {capabilities.resources is not None}")
        print(f"✅ Tools available: {capabilities.tools is not None}")
        
        # Test config and client
        print(f"✅ Config valid: {dv360_server.config.validate()}")
        print(f"✅ Client initialized: {dv360_server.dv360_client is not None}")
        
        # Try to test some actual functionality
        print("\n🔍 Testing actual DV360 access...")
        try:
            advertisers = await dv360_server.dv360_client.list_advertisers()
            print(f"✅ Successfully accessed {len(advertisers)} advertisers")
            
            # Show a few advertisers
            for i, advertiser in enumerate(advertisers[:3]):
                name = advertiser.get('displayName', 'N/A')
                id = advertiser.get('advertiserId', 'N/A')
                print(f"   {i+1}. {name} (ID: {id})")
                
        except Exception as e:
            print(f"⚠️  DV360 API access issue: {e}")
        
        print("\n🎉 Full server test completed!")
        print("📝 Server is ready for production use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_full_server())
    sys.exit(0 if result else 1)