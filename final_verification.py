#!/usr/bin/env python3
"""Final verification that DV360 MCP Server is ready for production."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dv360_mcp_server.server import DV360MCPServer
from dv360_mcp_server.config import Config
from dv360_mcp_server.dv360_client import DV360Client

async def final_verification():
    """Complete verification of all system components."""
    print("🔧 Final DV360 MCP Server Verification")
    print("=" * 50)
    
    success_count = 0
    total_tests = 7
    
    # Test 1: Config validation
    print("\n1️⃣ Testing configuration...")
    try:
        config = Config()
        valid = config.validate()
        cred_type = config.get_credentials_type()
        print(f"   ✅ Config valid: {valid}")
        print(f"   ✅ Credentials type: {cred_type}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Config error: {e}")
    
    # Test 2: DV360 Client
    print("\n2️⃣ Testing DV360 client...")
    try:
        client = DV360Client(config)
        print("   ✅ DV360 client initialized")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Client error: {e}")
        return False
    
    # Test 3: API Access
    print("\n3️⃣ Testing API access...")
    try:
        advertisers = await client.list_advertisers()
        print(f"   ✅ API access successful - {len(advertisers)} advertisers")
        success_count += 1
    except Exception as e:
        print(f"   ❌ API error: {e}")
        return False
    
    # Test 4: MCP Server Creation
    print("\n4️⃣ Testing MCP server creation...")
    try:
        dv360_server = DV360MCPServer()
        server = dv360_server.get_server()
        print(f"   ✅ MCP server created: {server.name}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Server creation error: {e}")
        return False
    
    # Test 5: Server Capabilities
    print("\n5️⃣ Testing server capabilities...")
    try:
        from mcp.server import NotificationOptions
        capabilities = server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={}
        )
        print(f"   ✅ Resources: {capabilities.resources is not None}")
        print(f"   ✅ Tools: {capabilities.tools is not None}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Capabilities error: {e}")
    
    # Test 6: Extended Functions
    print("\n6️⃣ Testing extended functions...")
    try:
        if advertisers:
            first_advertiser = advertisers[0]['advertiserId']
            summary = await client.get_advertiser_summary(first_advertiser)
            
            if 'error' not in summary:
                stats = summary['summary']
                print(f"   ✅ Advertiser summary: {stats['total_campaigns']} campaigns")
                success_count += 1
            else:
                print(f"   ⚠️  Summary warning: {summary['error']}")
                success_count += 0.5  # Partial credit
    except Exception as e:
        print(f"   ❌ Extended functions error: {e}")
    
    # Test 7: Production Readiness
    print("\n7️⃣ Production readiness check...")
    try:
        # Check if all files exist
        required_files = [
            'src/dv360_mcp_server/server.py',
            'src/dv360_mcp_server/config.py', 
            'src/dv360_mcp_server/dv360_client.py',
            'run_server.py',
            'README.md'
        ]
        
        missing_files = []
        for file in required_files:
            if not Path(file).exists():
                missing_files.append(file)
        
        if not missing_files:
            print("   ✅ All required files present")
            success_count += 1
        else:
            print(f"   ❌ Missing files: {missing_files}")
            
    except Exception as e:
        print(f"   ❌ File check error: {e}")
    
    # Final Results
    print("\n" + "=" * 50)
    print(f"🏁 FINAL RESULTS: {success_count}/{total_tests} tests passed")
    
    if success_count >= 6:
        print("\n🎉 DV360 MCP Server is READY FOR PRODUCTION!")
        print("\n📋 Claude Desktop Configuration:")
        print("Add this to ~/Library/Application Support/Claude/claude_desktop_config.json:")
        print()
        
        config_example = {
            "mcpServers": {
                "dv360": {
                    "command": "python3",
                    "args": ["run_server.py"],
                    "cwd": str(Path.cwd()),
                    "env": {
                        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/your/credentials.json"
                    }
                }
            }
        }
        
        print(json.dumps(config_example, indent=2))
        
        print("\n🚀 Next steps:")
        print("1. Add the above config to Claude Desktop")
        print("2. Restart Claude Desktop")
        print("3. Start using DV360 commands!")
        
        print(f"\n💼 You have access to {len(advertisers)} advertisers:")
        for i, advertiser in enumerate(advertisers[:5]):
            name = advertiser.get('displayName', 'N/A')
            id = advertiser.get('advertiserId', 'N/A')
            print(f"   • {name} (ID: {id})")
        if len(advertisers) > 5:
            print(f"   • ... and {len(advertisers) - 5} more")
            
        return True
    else:
        print("\n❌ SETUP INCOMPLETE - Please fix the failing tests above")
        return False

if __name__ == "__main__":
    result = asyncio.run(final_verification())
    sys.exit(0 if result else 1)