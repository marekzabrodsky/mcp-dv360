#!/usr/bin/env python3
"""
Google Display & Video 360 MCP Server

This server provides MCP (Model Context Protocol) integration for Google Display & Video 360 API,
enabling AI assistants to interact with DV360 programmatically.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    LoggingLevel
)

from .dv360_client import DV360Client
from .config import Config

logger = logging.getLogger(__name__)

class DV360MCPServer:
    def __init__(self):
        self.config = Config()
        self.dv360_client = DV360Client(self.config)
        
    def get_server(self) -> Server:
        """Create and configure the MCP server instance."""
        server = Server("dv360-mcp-server")
        
        # Register resources
        self._register_resources(server)
        
        # Register tools
        self._register_tools(server)
        
        return server
    
    def _register_resources(self, server: Server):
        """Register MCP resources for reading DV360 data."""
        
        @server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available DV360 resources."""
            return [
                Resource(
                    uri="dv360://advertisers",
                    name="Advertisers",
                    description="List of all advertisers in your DV360 account",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dv360://campaigns",
                    name="Campaigns",
                    description="List of all campaigns across advertisers",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dv360://line-items",
                    name="Line Items",
                    description="List of all line items",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dv360://audiences",
                    name="Audiences",
                    description="List of all audience segments",
                    mimeType="application/json"
                ),
                Resource(
                    uri="dv360://reports",
                    name="Reports",
                    description="Access to performance reports",
                    mimeType="application/json"
                )
            ]
        
        @server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read DV360 resource data."""
            try:
                if uri == "dv360://advertisers":
                    data = await self.dv360_client.list_advertisers()
                elif uri == "dv360://campaigns":
                    data = await self.dv360_client.list_campaigns()
                elif uri == "dv360://line-items":
                    data = await self.dv360_client.list_line_items()
                elif uri == "dv360://audiences":
                    data = await self.dv360_client.list_audiences()
                elif uri == "dv360://reports":
                    data = await self.dv360_client.list_reports()
                else:
                    raise ValueError(f"Unknown resource URI: {uri}")
                
                return str(data)
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                raise
    
    def _register_tools(self, server: Server):
        """Register MCP tools for DV360 operations."""
        
        @server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available DV360 tools."""
            return [
                Tool(
                    name="create_campaign",
                    description="Create a new advertising campaign",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID to create campaign under"
                            },
                            "campaign_name": {
                                "type": "string",
                                "description": "Name of the new campaign"
                            },
                            "campaign_goal": {
                                "type": "string",
                                "description": "Campaign goal (AWARENESS, CONSIDERATION, ACTION, etc.)"
                            }
                        },
                        "required": ["advertiser_id", "campaign_name", "campaign_goal"]
                    }
                ),
                Tool(
                    name="update_line_item_targeting",
                    description="Update targeting options for a line item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "line_item_id": {
                                "type": "string",
                                "description": "The line item ID to update"
                            },
                            "targeting_options": {
                                "type": "object",
                                "description": "Targeting configuration object"
                            }
                        },
                        "required": ["line_item_id", "targeting_options"]
                    }
                ),
                Tool(
                    name="get_campaign_performance",
                    description="Get performance metrics for a campaign",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "campaign_id": {
                                "type": "string",
                                "description": "Campaign ID to get performance for"
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, etc.)"
                            }
                        },
                        "required": ["campaign_id", "date_range"]
                    }
                ),
                Tool(
                    name="pause_line_item",
                    description="Pause a line item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "line_item_id": {
                                "type": "string",
                                "description": "Line item ID to pause"
                            }
                        },
                        "required": ["line_item_id"]
                    }
                ),
                Tool(
                    name="create_audience_list",
                    description="Create a new audience list",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "Advertiser ID to create audience under"
                            },
                            "audience_name": {
                                "type": "string",
                                "description": "Name of the audience list"
                            },
                            "audience_type": {
                                "type": "string",
                                "description": "Type of audience (FIRST_PARTY, THIRD_PARTY, etc.)"
                            }
                        },
                        "required": ["advertiser_id", "audience_name", "audience_type"]
                    }
                ),
                # Enhanced Information Tools
                Tool(
                    name="get_insertion_order_details",
                    description="Get detailed information about a specific insertion order including budget and settings",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "insertion_order_id": {
                                "type": "string",
                                "description": "The insertion order ID to get details for"
                            }
                        },
                        "required": ["advertiser_id", "insertion_order_id"]
                    }
                ),
                Tool(
                    name="get_line_item_details",
                    description="Get detailed information about a line item including budget, bidding strategy, and settings",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "line_item_id": {
                                "type": "string",
                                "description": "The line item ID to get details for"
                            }
                        },
                        "required": ["advertiser_id", "line_item_id"]
                    }
                ),
                Tool(
                    name="get_targeting_options",
                    description="Get targeting configuration for a specific line item",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "line_item_id": {
                                "type": "string",
                                "description": "The line item ID to get targeting for"
                            }
                        },
                        "required": ["advertiser_id", "line_item_id"]
                    }
                ),
                Tool(
                    name="get_campaign_performance_summary",
                    description="Get performance statistics for a campaign including impressions, clicks, CTR, conversions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "campaign_id": {
                                "type": "string",
                                "description": "Campaign ID to get performance for"
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, LAST_90_DAYS, etc.)",
                                "default": "LAST_30_DAYS"
                            }
                        },
                        "required": ["advertiser_id", "campaign_id"]
                    }
                ),
                Tool(
                    name="list_insertion_orders",
                    description="List insertion orders for an advertiser or specific campaign",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "campaign_id": {
                                "type": "string",
                                "description": "Optional: Filter by specific campaign ID"
                            }
                        },
                        "required": ["advertiser_id"]
                    }
                ),
                Tool(
                    name="list_line_items_for_io",
                    description="List line items for an advertiser or specific insertion order",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "insertion_order_id": {
                                "type": "string",
                                "description": "Optional: Filter by specific insertion order ID"
                            }
                        },
                        "required": ["advertiser_id"]
                    }
                ),
                Tool(
                    name="list_creatives",
                    description="List all creatives for an advertiser",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            }
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
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "creative_id": {
                                "type": "string",
                                "description": "The creative ID to get details for"
                            }
                        },
                        "required": ["advertiser_id", "creative_id"]
                    }
                ),
                Tool(
                    name="list_audiences_for_advertiser",
                    description="List audience segments for a specific advertiser",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            }
                        },
                        "required": ["advertiser_id"]
                    }
                ),
                Tool(
                    name="get_audience_details",
                    description="Get detailed information about an audience segment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "audience_id": {
                                "type": "string",
                                "description": "The audience ID to get details for"
                            }
                        },
                        "required": ["advertiser_id", "audience_id"]
                    }
                ),
                Tool(
                    name="list_saved_reports",
                    description="List all saved reports/queries",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "Optional: Filter by advertiser ID"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_advertiser_summary",
                    description="Get comprehensive summary of an advertiser with counts and recent activity",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID to get summary for"
                            }
                        },
                        "required": ["advertiser_id"]
                    }
                ),
                # REAL PERFORMANCE METRICS TOOLS
                Tool(
                    name="get_real_campaign_performance",
                    description="Get REAL performance metrics with actual impressions, clicks, CTR using Bid Manager API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "campaign_id": {
                                "type": "string",
                                "description": "Campaign ID to get real performance for"
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, LAST_90_DAYS, etc.)",
                                "default": "LAST_30_DAYS"
                            }
                        },
                        "required": ["advertiser_id", "campaign_id"]
                    }
                ),
                Tool(
                    name="get_real_advertiser_performance",
                    description="Get REAL performance summary for entire advertiser with actual metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, LAST_90_DAYS, etc.)",
                                "default": "LAST_30_DAYS"
                            }
                        },
                        "required": ["advertiser_id"]
                    }
                ),
                Tool(
                    name="get_real_line_item_performance",
                    description="Get REAL performance metrics for a specific line item with actual data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "line_item_id": {
                                "type": "string",
                                "description": "Line item ID to get real performance for"
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, LAST_90_DAYS, etc.)",
                                "default": "LAST_30_DAYS"
                            }
                        },
                        "required": ["advertiser_id", "line_item_id"]
                    }
                ),
                Tool(
                    name="create_custom_performance_report",
                    description="Create a custom performance report with specified metrics using Bid Manager API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "advertiser_id": {
                                "type": "string",
                                "description": "The advertiser ID"
                            },
                            "campaign_id": {
                                "type": "string",
                                "description": "Optional: Campaign ID to filter by"
                            },
                            "line_item_id": {
                                "type": "string",
                                "description": "Optional: Line item ID to filter by"
                            },
                            "date_range": {
                                "type": "string",
                                "description": "Date range (LAST_7_DAYS, LAST_30_DAYS, etc.)",
                                "default": "LAST_30_DAYS"
                            },
                            "metrics": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional: Specific metrics to include (e.g., METRIC_IMPRESSIONS, METRIC_CLICKS, METRIC_CTR)"
                            }
                        },
                        "required": ["advertiser_id"]
                    }
                ),
                Tool(
                    name="get_performance_report_data",
                    description="Get data from a performance report query",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query_id": {
                                "type": "string",
                                "description": "The query ID to get report data from"
                            }
                        },
                        "required": ["query_id"]
                    }
                ),
                Tool(
                    name="list_performance_queries",
                    description="List existing performance queries/reports",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_available_performance_metrics",
                    description="Get list of all available performance metrics (impressions, clicks, CTR, etc.)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_available_date_ranges",
                    description="Get list of all available date ranges for reports",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "create_campaign":
                    result = await self.dv360_client.create_campaign(
                        arguments["advertiser_id"],
                        arguments["campaign_name"],
                        arguments["campaign_goal"]
                    )
                elif name == "update_line_item_targeting":
                    result = await self.dv360_client.update_line_item_targeting(
                        arguments["line_item_id"],
                        arguments["targeting_options"]
                    )
                elif name == "get_campaign_performance":
                    result = await self.dv360_client.get_campaign_performance(
                        arguments["campaign_id"],
                        arguments["date_range"]
                    )
                elif name == "pause_line_item":
                    result = await self.dv360_client.pause_line_item(
                        arguments["line_item_id"]
                    )
                elif name == "create_audience_list":
                    result = await self.dv360_client.create_audience_list(
                        arguments["advertiser_id"],
                        arguments["audience_name"],
                        arguments["audience_type"]
                    )
                # Enhanced Information Tools
                elif name == "get_insertion_order_details":
                    result = await self.dv360_client.get_insertion_order_details(
                        arguments["advertiser_id"],
                        arguments["insertion_order_id"]
                    )
                elif name == "get_line_item_details":
                    result = await self.dv360_client.get_line_item_details(
                        arguments["advertiser_id"],
                        arguments["line_item_id"]
                    )
                elif name == "get_targeting_options":
                    result = await self.dv360_client.get_targeting_options(
                        arguments["advertiser_id"],
                        arguments["line_item_id"]
                    )
                elif name == "get_campaign_performance_summary":
                    date_range = arguments.get("date_range", "LAST_30_DAYS")
                    result = await self.dv360_client.get_campaign_performance_summary(
                        arguments["advertiser_id"],
                        arguments["campaign_id"],
                        date_range
                    )
                elif name == "list_insertion_orders":
                    campaign_id = arguments.get("campaign_id")
                    result = await self.dv360_client.list_insertion_orders(
                        arguments["advertiser_id"],
                        campaign_id
                    )
                elif name == "list_line_items_for_io":
                    insertion_order_id = arguments.get("insertion_order_id")
                    result = await self.dv360_client.list_line_items_for_io(
                        arguments["advertiser_id"],
                        insertion_order_id
                    )
                elif name == "list_creatives":
                    result = await self.dv360_client.list_creatives(
                        arguments["advertiser_id"]
                    )
                elif name == "get_creative_details":
                    result = await self.dv360_client.get_creative_details(
                        arguments["advertiser_id"],
                        arguments["creative_id"]
                    )
                elif name == "list_audiences_for_advertiser":
                    result = await self.dv360_client.list_audiences_for_advertiser(
                        arguments["advertiser_id"]
                    )
                elif name == "get_audience_details":
                    result = await self.dv360_client.get_audience_details(
                        arguments["advertiser_id"],
                        arguments["audience_id"]
                    )
                elif name == "list_saved_reports":
                    advertiser_id = arguments.get("advertiser_id")
                    result = await self.dv360_client.list_saved_reports(advertiser_id)
                elif name == "get_advertiser_summary":
                    result = await self.dv360_client.get_advertiser_summary(
                        arguments["advertiser_id"]
                    )
                # REAL PERFORMANCE METRICS HANDLERS
                elif name == "get_real_campaign_performance":
                    date_range = arguments.get("date_range", "LAST_30_DAYS")
                    result = await self.dv360_client.get_real_campaign_performance(
                        arguments["advertiser_id"],
                        arguments["campaign_id"],
                        date_range
                    )
                elif name == "get_real_advertiser_performance":
                    date_range = arguments.get("date_range", "LAST_30_DAYS")
                    result = await self.dv360_client.get_real_advertiser_performance(
                        arguments["advertiser_id"],
                        date_range
                    )
                elif name == "get_real_line_item_performance":
                    date_range = arguments.get("date_range", "LAST_30_DAYS")
                    result = await self.dv360_client.get_real_line_item_performance(
                        arguments["advertiser_id"],
                        arguments["line_item_id"],
                        date_range
                    )
                elif name == "create_custom_performance_report":
                    campaign_id = arguments.get("campaign_id")
                    line_item_id = arguments.get("line_item_id")
                    date_range = arguments.get("date_range", "LAST_30_DAYS")
                    metrics = arguments.get("metrics")
                    result = await self.dv360_client.create_custom_performance_report(
                        arguments["advertiser_id"],
                        campaign_id,
                        line_item_id,
                        date_range,
                        metrics
                    )
                elif name == "get_performance_report_data":
                    result = await self.dv360_client.get_performance_report_data(
                        arguments["query_id"]
                    )
                elif name == "list_performance_queries":
                    result = await self.dv360_client.list_performance_queries()
                elif name == "get_available_performance_metrics":
                    result = await self.dv360_client.get_available_performance_metrics()
                elif name == "get_available_date_ranges":
                    result = await self.dv360_client.get_available_date_ranges()
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the server."""
    # Don't use basicConfig as it can interfere with MCP
    logger = logging.getLogger(__name__)
    
    dv360_server = DV360MCPServer()
    server = dv360_server.get_server()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dv360-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())