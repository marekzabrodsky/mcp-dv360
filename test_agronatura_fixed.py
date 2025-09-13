#!/usr/bin/env python3
"""Test AgroNatura performance with fixed Bid Manager API parameters."""

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

async def test_agronatura_fixed():
    """Test AgroNatura with fixed API parameters."""
    print("🌱 Testing AgroNatura with Fixed API Parameters")
    print("=" * 50)
    
    try:
        # Initialize client
        config = Config()
        client = DV360Client(config)
        
        print("1️⃣ Finding AgroNatura advertiser...")
        advertisers = await client.list_advertisers()
        
        agronatura_advertiser = None
        for advertiser in advertisers:
            if 'agronatura' in advertiser['displayName'].lower():
                agronatura_advertiser = advertiser
                break
        
        if not agronatura_advertiser:
            print("   ❌ AgroNatura advertiser not found")
            return False
            
        advertiser_id = agronatura_advertiser['advertiserId']
        advertiser_name = agronatura_advertiser['displayName']
        
        print(f"   ✅ Found AgroNatura advertiser: {advertiser_name} (ID: {advertiser_id})")
        
        print("\n2️⃣ Getting AgroNatura campaigns...")
        campaigns = await client.list_campaigns_for_advertiser(advertiser_id)
        print(f"   ✅ Found {len(campaigns)} campaigns")
        
        if not campaigns:
            print("   ❌ No campaigns found")
            return False
        
        # Show all campaigns
        active_campaigns = []
        for i, campaign in enumerate(campaigns):
            campaign_name = campaign.get('displayName', 'N/A')
            campaign_id = campaign.get('campaignId', 'N/A')
            status = campaign.get('entityStatus', 'N/A')
            print(f"   {i+1}. {campaign_name} (ID: {campaign_id}) - {status}")
            
            if status == 'ENTITY_STATUS_ACTIVE':
                active_campaigns.append(campaign)
        
        if not active_campaigns:
            print("   ⚠️  No active campaigns found, testing with first campaign anyway...")
            test_campaign = campaigns[0]
        else:
            test_campaign = active_campaigns[0]
            
        campaign_id = test_campaign['campaignId']
        campaign_name = test_campaign['displayName']
        
        print(f"\n3️⃣ Testing performance for: {campaign_name}")
        print(f"   📊 Campaign ID: {campaign_id}")
        
        try:
            print("   🔍 Creating performance query for LAST_7_DAYS...")
            
            # Test with fixed API parameters
            performance_result = await client.get_real_campaign_performance(
                advertiser_id,
                campaign_id,
                "LAST_7_DAYS"
            )
            
            if 'error' in performance_result:
                print(f"   ❌ Performance query error: {performance_result['error']}")
            else:
                print("   ✅ SUCCESS! Performance query created!")
                print(f"   📊 Query ID: {performance_result.get('query_id', 'N/A')}")
                print(f"   📅 Date range: {performance_result.get('date_range', 'N/A')}")
                
                print(f"\n🎉 VÝBORNĚ! Performance query pro AgroNatura byla úspěšně vytvořena!")
                print(f"📊 Kampaň: {campaign_name}")
                print(f"📅 Období: Poslední týden")
                print(f"🔗 Query ID: {performance_result.get('query_id', 'N/A')}")
                
                print(f"\n💡 Co se nyní děje:")
                print(f"   1. Query se zpracovává v pozadí")
                print(f"   2. Google generuje report s reálnými daty")
                print(f"   3. Po dokončení budete mít přístup k:")
                print(f"      • Skutečné impressions (zobrazení)")
                print(f"      • Skutečné clicks (kliky)")
                print(f"      • Skutečná CTR (míra prokliku)")
                print(f"      • Skutečné conversion data")
                print(f"      • Skutečné spend (výdaje)")
                
                return True
                
        except Exception as e:
            print(f"   ❌ Chyba při vytváření performance query: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_agronatura_fixed())
    if result:
        print("\n🌱 AgroNatura performance test ÚSPĚŠNÝ!")
    else:
        print("\n❌ AgroNatura performance test NEÚSPĚŠNÝ")
    sys.exit(0 if result else 1)