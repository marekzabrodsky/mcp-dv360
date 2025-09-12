#!/usr/bin/env python3
"""Single file DV360 MCP Server"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))

# MCP imports
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent

# Our imports
from dv360_mcp_server.config import Config
from dv360_mcp_server.dv360_client import DV360Client

def create_server() -> Server:
    """Create the DV360 MCP server."""
    server = Server("dv360-mcp-server")
    config = Config()
    client = DV360Client(config)

    @server.list_resources()
    async def handle_list_resources():
        return [
            Resource(
                uri="dv360://advertisers",
                name="Advertisers",
                description="Your DV360 advertisers",
                mimeType="application/json"
            )
        ]

    @server.read_resource()
    async def handle_read_resource(uri: str) -> str:
        if uri == "dv360://advertisers":
            try:
                advertisers = await client.list_advertisers()
                result = f"Found {len(advertisers)} advertisers:\n\n"
                for i, advertiser in enumerate(advertisers[:10]):
                    name = advertiser.get('displayName', 'N/A')
                    id = advertiser.get('advertiserId', 'N/A')
                    result += f"{i+1}. {name} (ID: {id})\n"
                if len(advertisers) > 10:
                    result += f"\n... and {len(advertisers) - 10} more advertisers"
                return result
            except Exception as e:
                return f"Error loading advertisers: {str(e)}"
        return "Unknown resource"

    @server.list_tools()
    async def handle_list_tools():
        return [
            # Basic listing
            Tool(
                name="list_advertisers",
                description="List all DV360 advertisers",
                inputSchema={"type": "object", "properties": {}}
            ),
            Tool(
                name="get_advertiser_summary",
                description="Get comprehensive summary of an advertiser including campaigns, line items, creatives",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            
            # Campaign management
            Tool(
                name="list_campaigns",
                description="List campaigns for a specific advertiser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            Tool(
                name="list_active_campaigns",
                description="List only active campaigns for an advertiser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            Tool(
                name="search_campaigns",
                description="Search campaigns by name within an advertiser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "search_term": {"type": "string", "description": "Search term to find in campaign names"}
                    },
                    "required": ["advertiser_id", "search_term"]
                }
            ),
            Tool(
                name="get_campaign_details",
                description="Get detailed information about a specific campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "campaign_id": {"type": "string", "description": "Campaign ID"}
                    },
                    "required": ["advertiser_id", "campaign_id"]
                }
            ),
            
            # Insertion Orders
            Tool(
                name="list_insertion_orders",
                description="List insertion orders for advertiser or specific campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "campaign_id": {"type": "string", "description": "Campaign ID (optional)"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            Tool(
                name="get_insertion_order_details",
                description="Get detailed information about a specific insertion order",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "insertion_order_id": {"type": "string", "description": "Insertion Order ID"}
                    },
                    "required": ["advertiser_id", "insertion_order_id"]
                }
            ),
            
            # Line Items
            Tool(
                name="list_line_items",
                description="List line items for advertiser or specific insertion order",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "insertion_order_id": {"type": "string", "description": "Insertion Order ID (optional)"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            Tool(
                name="get_line_item_details",
                description="Get detailed information about a specific line item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "line_item_id": {"type": "string", "description": "Line Item ID"}
                    },
                    "required": ["advertiser_id", "line_item_id"]
                }
            ),
            Tool(
                name="get_targeting_options",
                description="Get targeting configuration for a line item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "line_item_id": {"type": "string", "description": "Line Item ID"}
                    },
                    "required": ["advertiser_id", "line_item_id"]
                }
            ),
            
            # Creatives
            Tool(
                name="list_creatives",
                description="List all creatives for an advertiser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            Tool(
                name="get_creative_details",
                description="Get detailed information about a specific creative",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "creative_id": {"type": "string", "description": "Creative ID"}
                    },
                    "required": ["advertiser_id", "creative_id"]
                }
            ),
            
            # Audiences
            Tool(
                name="list_audiences",
                description="List audience segments for an advertiser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"}
                    },
                    "required": ["advertiser_id"]
                }
            ),
            Tool(
                name="get_audience_details",
                description="Get detailed information about an audience",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "audience_id": {"type": "string", "description": "Audience ID"}
                    },
                    "required": ["advertiser_id", "audience_id"]
                }
            ),
            
            # Reporting
            Tool(
                name="get_campaign_performance_summary",
                description="Get quick performance overview for a campaign",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID"},
                        "campaign_id": {"type": "string", "description": "Campaign ID"},
                        "date_range": {"type": "string", "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, etc.)", "default": "LAST_30_DAYS"}
                    },
                    "required": ["advertiser_id", "campaign_id"]
                }
            ),
            Tool(
                name="list_saved_reports",
                description="List saved reports, optionally filtered by advertiser",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "advertiser_id": {"type": "string", "description": "Advertiser ID (optional)"}
                    }
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict):
        try:
            if name == "list_advertisers":
                advertisers = await client.list_advertisers()
                result = f"✅ Found {len(advertisers)} advertisers in your DV360 account:\n\n"
                
                for i, advertiser in enumerate(advertisers[:15]):
                    name = advertiser.get('displayName', 'N/A')
                    id = advertiser.get('advertiserId', 'N/A')
                    status = advertiser.get('entityStatus', 'N/A')
                    result += f"{i+1:2d}. {name} (ID: {id}) - {status}\n"
                    
                if len(advertisers) > 15:
                    result += f"\n... and {len(advertisers) - 15} more advertisers"
                    
                result += f"\n📊 Total: {len(advertisers)} advertisers"
                return [TextContent(type="text", text=result)]
            
            elif name == "get_advertiser_summary":
                advertiser_id = arguments["advertiser_id"]
                summary = await client.get_advertiser_summary(advertiser_id)
                
                if 'error' in summary:
                    return [TextContent(type="text", text=f"❌ Error: {summary['error']}")]
                
                adv = summary['advertiser']
                stats = summary['summary']
                result = f"📊 **{adv.get('displayName', 'N/A')}** (ID: {advertiser_id})\n\n"
                result += f"📈 **Summary:**\n"
                result += f"• Total Campaigns: {stats['total_campaigns']}\n"
                result += f"• Active Campaigns: {stats['active_campaigns']}\n"
                result += f"• Insertion Orders: {stats['insertion_orders']}\n"
                result += f"• Line Items: {stats['line_items']}\n"
                result += f"• Creatives: {stats['creatives']}\n"
                
                if summary['recent_campaigns']:
                    result += f"\n🎯 **Recent Campaigns:**\n"
                    for i, camp in enumerate(summary['recent_campaigns'][:5]):
                        result += f"{i+1}. {camp.get('displayName', 'N/A')} (ID: {camp.get('campaignId', 'N/A')})\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_campaigns":
                advertiser_id = arguments["advertiser_id"]
                campaigns = await client.list_campaigns_for_advertiser(advertiser_id)
                
                result = f"🎯 Found {len(campaigns)} campaigns for advertiser {advertiser_id}:\n\n"
                for i, campaign in enumerate(campaigns[:20]):
                    name = campaign.get('displayName', 'N/A')
                    id = campaign.get('campaignId', 'N/A')
                    status = campaign.get('entityStatus', 'N/A')
                    goal = campaign.get('campaignGoal', {}).get('campaignGoalType', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Status: {status} | Goal: {goal}\n\n"
                
                if len(campaigns) > 20:
                    result += f"... and {len(campaigns) - 20} more campaigns"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_active_campaigns":
                advertiser_id = arguments["advertiser_id"]
                campaigns = await client.list_active_campaigns(advertiser_id)
                
                result = f"🟢 Found {len(campaigns)} active campaigns for advertiser {advertiser_id}:\n\n"
                for i, campaign in enumerate(campaigns):
                    name = campaign.get('displayName', 'N/A')
                    id = campaign.get('campaignId', 'N/A')
                    goal = campaign.get('campaignGoal', {}).get('campaignGoalType', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Goal: {goal}\n\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "search_campaigns":
                advertiser_id = arguments["advertiser_id"]
                search_term = arguments["search_term"]
                campaigns = await client.search_campaigns(advertiser_id, search_term)
                
                result = f"🔍 Found {len(campaigns)} campaigns matching '{search_term}':\n\n"
                for i, campaign in enumerate(campaigns):
                    name = campaign.get('displayName', 'N/A')
                    id = campaign.get('campaignId', 'N/A')
                    status = campaign.get('entityStatus', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Status: {status}\n\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "get_campaign_details":
                advertiser_id = arguments["advertiser_id"]
                campaign_id = arguments["campaign_id"]
                campaign = await client.get_campaign_details(advertiser_id, campaign_id)
                
                result = f"🎯 **Campaign Details:**\n\n"
                result += f"**Name:** {campaign.get('displayName', 'N/A')}\n"
                result += f"**ID:** {campaign.get('campaignId', 'N/A')}\n"
                result += f"**Status:** {campaign.get('entityStatus', 'N/A')}\n"
                result += f"**Goal:** {campaign.get('campaignGoal', {}).get('campaignGoalType', 'N/A')}\n"
                if campaign.get('updateTime'):
                    result += f"**Updated:** {campaign.get('updateTime')}\n"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_insertion_orders":
                advertiser_id = arguments["advertiser_id"]
                campaign_id = arguments.get("campaign_id")
                ios = await client.list_insertion_orders(advertiser_id, campaign_id)
                
                filter_text = f" for campaign {campaign_id}" if campaign_id else ""
                result = f"📋 Found {len(ios)} insertion orders{filter_text}:\n\n"
                
                for i, io in enumerate(ios[:15]):
                    name = io.get('displayName', 'N/A')
                    id = io.get('insertionOrderId', 'N/A')
                    status = io.get('entityStatus', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Status: {status}\n\n"
                
                if len(ios) > 15:
                    result += f"... and {len(ios) - 15} more insertion orders"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_line_items":
                advertiser_id = arguments["advertiser_id"]
                insertion_order_id = arguments.get("insertion_order_id")
                line_items = await client.list_line_items_for_io(advertiser_id, insertion_order_id)
                
                filter_text = f" for insertion order {insertion_order_id}" if insertion_order_id else ""
                result = f"📝 Found {len(line_items)} line items{filter_text}:\n\n"
                
                for i, li in enumerate(line_items[:15]):
                    name = li.get('displayName', 'N/A')
                    id = li.get('lineItemId', 'N/A')
                    status = li.get('entityStatus', 'N/A')
                    type = li.get('lineItemType', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Status: {status} | Type: {type}\n\n"
                
                if len(line_items) > 15:
                    result += f"... and {len(line_items) - 15} more line items"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_creatives":
                advertiser_id = arguments["advertiser_id"]
                creatives = await client.list_creatives(advertiser_id)
                
                result = f"🎨 Found {len(creatives)} creatives for advertiser {advertiser_id}:\n\n"
                
                for i, creative in enumerate(creatives[:15]):
                    name = creative.get('displayName', 'N/A')
                    id = creative.get('creativeId', 'N/A')
                    status = creative.get('entityStatus', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Status: {status}\n\n"
                
                if len(creatives) > 15:
                    result += f"... and {len(creatives) - 15} more creatives"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_audiences":
                advertiser_id = arguments["advertiser_id"]
                audiences = await client.list_audiences_for_advertiser(advertiser_id)
                
                result = f"👥 Found {len(audiences)} audiences for advertiser {advertiser_id}:\n\n"
                
                for i, audience in enumerate(audiences[:15]):
                    name = audience.get('displayName', 'N/A')
                    id = audience.get('firstAndThirdPartyAudienceId', 'N/A')
                    type = audience.get('audienceType', 'N/A')
                    size = audience.get('membershipDurationDays', 'N/A')
                    result += f"{i+1:2d}. {name}\n    ID: {id} | Type: {type} | Duration: {size} days\n\n"
                
                if len(audiences) > 15:
                    result += f"... and {len(audiences) - 15} more audiences"
                
                return [TextContent(type="text", text=result)]
            
            elif name == "get_campaign_performance_summary":
                advertiser_id = arguments["advertiser_id"]
                campaign_id = arguments["campaign_id"]
                date_range = arguments.get("date_range", "LAST_30_DAYS")
                
                summary = await client.get_campaign_performance_summary(advertiser_id, campaign_id, date_range)
                
                if 'error' in summary:
                    return [TextContent(type="text", text=f"❌ Error: {summary['error']}")]
                
                campaign_name = summary['campaign'].get('displayName', 'N/A')
                result = f"📈 **Performance Summary: {campaign_name}**\n\n"
                result += f"**Campaign ID:** {campaign_id}\n"
                result += f"**Date Range:** {date_range}\n"
                result += f"**Report Status:** {summary['status']}\n"
                result += f"**Query ID:** {summary['report_query_id']}\n\n"
                result += "ℹ️ Report generation initiated. Use the query ID to check status and download data later."
                
                return [TextContent(type="text", text=result)]
            
            elif name == "list_saved_reports":
                advertiser_id = arguments.get("advertiser_id")
                reports = await client.list_saved_reports(advertiser_id)
                
                filter_text = f" for advertiser {advertiser_id}" if advertiser_id else ""
                result = f"📊 Found {len(reports)} saved reports{filter_text}:\n\n"
                
                for i, report in enumerate(reports[:10]):
                    title = report.get('metadata', {}).get('title', 'N/A')
                    id = report.get('queryId', 'N/A')
                    format = report.get('metadata', {}).get('format', 'N/A')
                    result += f"{i+1:2d}. {title}\n    ID: {id} | Format: {format}\n\n"
                
                if len(reports) > 10:
                    result += f"... and {len(reports) - 10} more reports"
                
                return [TextContent(type="text", text=result)]
            
            else:
                return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
                
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

    return server

async def main():
    """Main entry point."""
    server = create_server()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dv360-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())