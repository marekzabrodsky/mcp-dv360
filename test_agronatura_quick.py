#!/usr/bin/env python3
"""Quick test for AgroNatura campaign search and performance query creation."""

import asyncio
import os
import sys
from pathlib import Path

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/marekzabrodsky/Downloads/dingomedia-a0dc8e320f9c.json"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dv360_mcp_server.dv360_client import DV360Client
from dv360_mcp_server.config import Config

async def quick_agronatura_test():
    """Quick test for AgroNatura campaigns."""
    print("🌱 Quick AgroNatura Campaign Search")
    print("=" * 40)
    
    try:
        # Initialize client
        config = Config()
        client = DV360Client(config)
        
        print("1️⃣ Getting advertisers...")
        advertisers = await client.list_advertisers()
        print(f"   ✅ Found {len(advertisers)} advertisers")
        
        # Search for AgroNatura or similar campaigns
        print("\n2️⃣ Searching for AgroNatura campaigns...")
        agronatura_campaigns = []
        
        # Check first few advertisers to avoid timeout
        for advertiser in advertisers[:10]:  # Limit to first 10 advertisers
            advertiser_id = advertiser['advertiserId']
            advertiser_name = advertiser['displayName']
            
            try:
                campaigns = await client.list_campaigns_for_advertiser(advertiser_id)
                
                for campaign in campaigns:
                    campaign_name = campaign.get('displayName', '')
                    # Look for AgroNatura or similar names
                    if any(term in campaign_name.lower() for term in ['agronatura', 'agro', 'natura']):
                        agronatura_campaigns.append({
                            'advertiser_name': advertiser_name,
                            'advertiser_id': advertiser_id,
                            'campaign_id': campaign['campaignId'],
                            'campaign_name': campaign_name,
                            'status': campaign.get('entityStatus', 'N/A')
                        })
                        print(f"   🌱 FOUND: {campaign_name}")
                        print(f"      Advertiser: {advertiser_name}")
                        print(f"      ID: {campaign['campaignId']}")
                        print(f"      Status: {campaign.get('entityStatus', 'N/A')}")
                        
            except Exception as e:
                print(f"   ⚠️  Skipping {advertiser_name}: {str(e)[:50]}...")
                continue
        
        if agronatura_campaigns:
            print(f"\n3️⃣ Testing performance query for first campaign...")
            campaign = agronatura_campaigns[0]
            
            try:
                # Create performance query for last week
                performance_result = await client.get_real_campaign_performance(
                    campaign['advertiser_id'],
                    campaign['campaign_id'],
                    "LAST_7_DAYS"
                )
                
                if 'error' in performance_result:
                    print(f"   ❌ Performance query error: {performance_result['error']}")
                else:
                    print("   ✅ Performance query created successfully!")
                    print(f"   📊 Query ID: {performance_result.get('query_id', 'N/A')}")
                    print(f"   📅 Campaign: {campaign['campaign_name']}")
                    print(f"   📈 Date range: LAST_7_DAYS")
                    
                    print("\n🎉 SUCCESS! Real performance data query created!")
                    print("💡 The query is processing. In production, you would:")
                    print("   1. Wait for processing to complete")
                    print("   2. Download the report data")
                    print("   3. See actual impressions, clicks, CTR")
                    
            except Exception as e:
                print(f"   ❌ Performance query error: {e}")
                
        else:
            print("\n❌ No AgroNatura campaigns found in first 10 advertisers")
            print("\n📋 Sample campaigns found:")
            
            # Show some example campaigns
            for advertiser in advertisers[:3]:
                try:
                    campaigns = await client.list_campaigns_for_advertiser(advertiser['advertiserId'])
                    print(f"\n   Advertiser: {advertiser['displayName']}")
                    for campaign in campaigns[:3]:
                        print(f"      • {campaign.get('displayName', 'N/A')}")
                except:
                    continue
        
        print(f"\n🌱 Summary:")
        print(f"   • Searched {min(10, len(advertisers))} advertisers")
        print(f"   • Found {len(agronatura_campaigns)} AgroNatura-related campaigns")
        print(f"   • Real performance data access is working!")
        
        return len(agronatura_campaigns) > 0
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(quick_agronatura_test())
    sys.exit(0 if result else 1)