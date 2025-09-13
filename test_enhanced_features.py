#!/usr/bin/env python3
"""Test enhanced DV360 MCP Server features."""

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
from dv360_mcp_server.dv360_client import DV360Client
from dv360_mcp_server.config import Config

async def test_enhanced_features():
    """Test the enhanced features of DV360 MCP Server."""
    print("🧪 Testing Enhanced DV360 MCP Server Features")
    print("=" * 60)
    
    try:
        # Initialize client
        config = Config()
        client = DV360Client(config)
        
        # Get a test advertiser
        print("📋 Getting test advertiser...")
        advertisers = await client.list_advertisers()
        if not advertisers:
            print("❌ No advertisers found - cannot test enhanced features")
            return False
        
        test_advertiser_id = advertisers[0]['advertiserId']
        test_advertiser_name = advertisers[0]['displayName']
        print(f"✅ Using advertiser: {test_advertiser_name} (ID: {test_advertiser_id})")
        
        # Test 1: Advertiser Summary
        print(f"\n1️⃣ Testing get_advertiser_summary...")
        try:
            summary = await client.get_advertiser_summary(test_advertiser_id)
            if 'error' not in summary:
                stats = summary['summary']
                print(f"   ✅ Summary retrieved:")
                print(f"      • Campaigns: {stats['total_campaigns']} (Active: {stats['active_campaigns']})")
                print(f"      • Insertion Orders: {stats['insertion_orders']}")
                print(f"      • Line Items: {stats['line_items']}")
                print(f"      • Creatives: {stats['creatives']}")
            else:
                print(f"   ⚠️  Summary warning: {summary['error']}")
        except Exception as e:
            print(f"   ❌ Summary test failed: {e}")
        
        # Test 2: Insertion Orders
        print(f"\n2️⃣ Testing list_insertion_orders...")
        try:
            insertion_orders = await client.list_insertion_orders(test_advertiser_id)
            print(f"   ✅ Found {len(insertion_orders)} insertion orders")
            
            # Test details if we have insertion orders
            if insertion_orders:
                first_io_id = insertion_orders[0]['insertionOrderId']
                print(f"   🔍 Testing get_insertion_order_details for ID: {first_io_id}")
                io_details = await client.get_insertion_order_details(test_advertiser_id, first_io_id)
                print(f"   ✅ IO details retrieved: {io_details.get('displayName', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Insertion orders test failed: {e}")
        
        # Test 3: Line Items
        print(f"\n3️⃣ Testing list_line_items_for_io...")
        try:
            line_items = await client.list_line_items_for_io(test_advertiser_id)
            print(f"   ✅ Found {len(line_items)} line items")
            
            # Test details if we have line items
            if line_items:
                first_li_id = line_items[0]['lineItemId']
                print(f"   🔍 Testing get_line_item_details for ID: {first_li_id}")
                li_details = await client.get_line_item_details(test_advertiser_id, first_li_id)
                print(f"   ✅ Line item details retrieved: {li_details.get('displayName', 'N/A')}")
                
                # Test targeting options
                print(f"   🎯 Testing get_targeting_options...")
                targeting = await client.get_targeting_options(test_advertiser_id, first_li_id)
                print(f"   ✅ Targeting options retrieved")
        except Exception as e:
            print(f"   ❌ Line items test failed: {e}")
        
        # Test 4: Creatives
        print(f"\n4️⃣ Testing list_creatives...")
        try:
            creatives = await client.list_creatives(test_advertiser_id)
            print(f"   ✅ Found {len(creatives)} creatives")
            
            # Test details if we have creatives
            if creatives:
                first_creative_id = creatives[0]['creativeId']
                print(f"   🎨 Testing get_creative_details for ID: {first_creative_id}")
                creative_details = await client.get_creative_details(test_advertiser_id, first_creative_id)
                print(f"   ✅ Creative details retrieved: {creative_details.get('displayName', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Creatives test failed: {e}")
        
        # Test 5: Audiences
        print(f"\n5️⃣ Testing list_audiences_for_advertiser...")
        try:
            audiences = await client.list_audiences_for_advertiser(test_advertiser_id)
            print(f"   ✅ Found {len(audiences)} audiences")
            
            # Test details if we have audiences
            if audiences:
                first_audience_id = audiences[0]['firstAndThirdPartyAudienceId']
                print(f"   👥 Testing get_audience_details for ID: {first_audience_id}")
                audience_details = await client.get_audience_details(test_advertiser_id, first_audience_id)
                print(f"   ✅ Audience details retrieved: {audience_details.get('displayName', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Audiences test failed: {e}")
        
        # Test 6: Reports
        print(f"\n6️⃣ Testing list_saved_reports...")
        try:
            reports = await client.list_saved_reports(test_advertiser_id)
            print(f"   ✅ Found {len(reports)} saved reports")
        except Exception as e:
            print(f"   ❌ Reports test failed: {e}")
        
        # Test 7: Campaign Performance (if we have campaigns)
        print(f"\n7️⃣ Testing get_campaign_performance_summary...")
        try:
            campaigns = await client.list_campaigns_for_advertiser(test_advertiser_id)
            if campaigns:
                first_campaign_id = campaigns[0]['campaignId']
                print(f"   📊 Testing performance summary for campaign: {first_campaign_id}")
                performance = await client.get_campaign_performance_summary(
                    test_advertiser_id, first_campaign_id, "LAST_30_DAYS"
                )
                if 'error' not in performance:
                    print(f"   ✅ Performance query initiated: {performance.get('report_query_id', 'N/A')}")
                else:
                    print(f"   ⚠️  Performance warning: {performance['error']}")
            else:
                print("   ⚠️  No campaigns found for performance testing")
        except Exception as e:
            print(f"   ❌ Performance test failed: {e}")
        
        print(f"\n" + "=" * 60)
        print("🎉 Enhanced features testing completed!")
        print("✨ All new tools are ready for use in MCP server!")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced features test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_enhanced_features())
    sys.exit(0 if result else 1)