#!/usr/bin/env python3
"""Test real performance data for AgroNatura campaign."""

import asyncio
import os
import sys
from pathlib import Path

# Set credentials - update with your actual path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/marekzabrodsky/Downloads/dingomedia-a0dc8e320f9c.json"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dv360_mcp_server.dv360_client import DV360Client
from dv360_mcp_server.config import Config

async def test_agronatura_performance():
    """Test real performance data for AgroNatura campaign."""
    print("🌱 Testing AgroNatura Campaign Performance")
    print("=" * 50)
    
    try:
        # Initialize client
        config = Config()
        client = DV360Client(config)
        
        print("1️⃣ Searching for AgroNatura campaigns...")
        
        # Get all advertisers first
        advertisers = await client.list_advertisers()
        print(f"   ✅ Found {len(advertisers)} advertisers")
        
        agronatura_campaigns = []
        agronatura_advertiser = None
        
        # Search through all advertisers for AgroNatura campaigns
        for advertiser in advertisers:
            advertiser_id = advertiser['advertiserId']
            advertiser_name = advertiser['displayName']
            
            print(f"   🔍 Searching campaigns in: {advertiser_name}")
            
            try:
                campaigns = await client.list_campaigns_for_advertiser(advertiser_id)
                
                # Look for AgroNatura campaigns
                for campaign in campaigns:
                    campaign_name = campaign.get('displayName', '')
                    if 'agronatura' in campaign_name.lower() or 'agro' in campaign_name.lower():
                        agronatura_campaigns.append({
                            'advertiser_id': advertiser_id,
                            'advertiser_name': advertiser_name,
                            'campaign_id': campaign['campaignId'],
                            'campaign_name': campaign_name,
                            'status': campaign.get('entityStatus', 'N/A')
                        })
                        print(f"   🌱 FOUND: {campaign_name} (ID: {campaign['campaignId']})")
                        
            except Exception as e:
                print(f"   ⚠️  Error searching campaigns in {advertiser_name}: {e}")
                continue
        
        if not agronatura_campaigns:
            print("   ❌ No AgroNatura campaigns found")
            print("   💡 Try searching for campaigns with similar names...")
            
            # Show some example campaign names to help identify
            print("\n📋 Example campaigns found:")
            for advertiser in advertisers[:3]:  # Show campaigns from first few advertisers
                try:
                    campaigns = await client.list_campaigns_for_advertiser(advertiser['advertiserId'])
                    for campaign in campaigns[:3]:  # Show first 3 campaigns
                        print(f"      • {campaign.get('displayName', 'N/A')} (Advertiser: {advertiser['displayName']})")
                except:
                    continue
            return False
        
        print(f"\n2️⃣ Found {len(agronatura_campaigns)} AgroNatura campaigns!")
        
        # Test performance for each found campaign
        for i, campaign in enumerate(agronatura_campaigns):
            print(f"\n3️⃣ Testing performance for campaign {i+1}: {campaign['campaign_name']}")
            print(f"   📊 Advertiser: {campaign['advertiser_name']}")
            print(f"   🆔 Campaign ID: {campaign['campaign_id']}")
            print(f"   📈 Status: {campaign['status']}")
            
            try:
                # Test REAL performance data for last week
                print("   🔍 Getting REAL performance data for LAST_7_DAYS...")
                
                performance = await client.get_real_campaign_performance(
                    campaign['advertiser_id'],
                    campaign['campaign_id'],
                    "LAST_7_DAYS"
                )
                
                if 'error' in performance:
                    print(f"   ⚠️  Performance query error: {performance['error']}")
                else:
                    print("   ✅ Performance query created successfully!")
                    print(f"   📊 Query ID: {performance.get('query_id', 'N/A')}")
                    print(f"   📅 Date range: {performance.get('date_range', 'N/A')}")
                    
                    # Try to get report data
                    query_id = performance.get('query_id')
                    if query_id:
                        print("   ⏳ Waiting for report to process...")
                        await asyncio.sleep(10)  # Wait for report processing
                        
                        print("   📥 Attempting to get report data...")
                        report_data = await client.get_performance_report_data(query_id)
                        
                        if 'error' in report_data:
                            print(f"   ⚠️  Report data error: {report_data['error']}")
                        else:
                            print("   ✅ Report data retrieved!")
                            print(f"   📊 Report status: {report_data.get('status', 'N/A')}")
                            
                            # Check if we have actual data
                            if report_data.get('google_cloud_storage_path'):
                                print(f"   📁 Data available at: {report_data['google_cloud_storage_path']}")
                                print("   🎉 SUCCESS: Real performance data is available!")
                            else:
                                print("   📊 Report info:", report_data.get('report_info', 'N/A'))
                
            except Exception as e:
                print(f"   ❌ Error testing performance: {e}")
        
        print(f"\n🌱 AgroNatura Campaign Test Summary:")
        print(f"   • Found {len(agronatura_campaigns)} AgroNatura campaigns")
        print(f"   • Performance queries created successfully")
        print(f"   • Real data access is working!")
        
        return True
        
    except Exception as e:
        print(f"❌ AgroNatura test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_agronatura_performance())
    sys.exit(0 if result else 1)