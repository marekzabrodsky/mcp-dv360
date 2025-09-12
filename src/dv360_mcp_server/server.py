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