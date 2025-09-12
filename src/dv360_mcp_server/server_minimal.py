#!/usr/bin/env python3
"""Minimal DV360 MCP Server for troubleshooting."""

import asyncio
import sys
from typing import Any, Dict, List

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent

from .config import Config
from .dv360_client import DV360Client

def create_server() -> Server:
    """Create a minimal MCP server."""
    server = Server("dv360-mcp-server")
    config = Config()
    client = DV360Client(config)

    @server.list_resources()
    async def handle_list_resources() -> List[Resource]:
        return [
            Resource(
                uri="dv360://advertisers",
                name="Advertisers",
                description="DV360 advertisers",
                mimeType="application/json"
            )
        ]

    @server.read_resource()
    async def handle_read_resource(uri: str) -> str:
        if uri == "dv360://advertisers":
            try:
                advertisers = await client.list_advertisers()
                return f"Found {len(advertisers)} advertisers"
            except Exception as e:
                return f"Error: {str(e)}"
        return "Unknown resource"

    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        return [
            Tool(
                name="list_advertisers",
                description="List DV360 advertisers",
                inputSchema={"type": "object", "properties": {}}
            )
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        if name == "list_advertisers":
            try:
                advertisers = await client.list_advertisers()
                result = f"Found {len(advertisers)} advertisers"
                if advertisers:
                    result += f"\nFirst few: {[a.get('displayName', 'N/A') for a in advertisers[:3]]}"
                return [TextContent(type="text", text=result)]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]
        
        return [TextContent(type="text", text="Unknown tool")]

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
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())