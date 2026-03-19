"""MCP server for Brazilian startup data — stdio transport."""

import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

load_dotenv()

# Ensure data directory exists
_db_path = os.environ.get("DUCKDB_PATH", "./data/cache.duckdb")
_data_dir = os.path.dirname(_db_path)
if _data_dir:
    os.makedirs(_data_dir, exist_ok=True)

server = Server("br-startup-mcp")

# Tool schemas
_CVM_SCHEMA = {
    "type": "object",
    "properties": {
        "cnpj": {
            "type": "string",
            "description": "Filter by issuer CNPJ (optional)",
        },
        "status": {
            "type": "string",
            "description": "Filter by offer status (optional, partial match)",
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of results (default 20)",
            "default": 20,
        },
    },
    "required": [],
}

_BNDES_SCHEMA = {
    "type": "object",
    "properties": {
        "cnpj": {
            "type": "string",
            "description": "Filter by client CNPJ (optional)",
        },
        "produto": {
            "type": "string",
            "description": "Filter by BNDES product name (optional, partial match)",
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of results (default 20)",
            "default": 20,
        },
    },
    "required": [],
}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_cvm_crowdfunding_offers",
            description=(
                "Fetch public offering data from CVM (Brazil's securities regulator) "
                "open data portal. Returns offers registered with CVM, including equity, "
                "debt, and fund offerings. Useful for due diligence on Brazilian companies "
                "that raised capital via public offerings."
            ),
            inputSchema=_CVM_SCHEMA,
        ),
        types.Tool(
            name="get_bndes_financing",
            description=(
                "Fetch BNDES (Brazil's national development bank) financing operations "
                "from the open data portal. Returns contracted financing operations "
                "with client name, product, value, and date. Useful for identifying "
                "startups and companies that received BNDES funding."
            ),
            inputSchema=_BNDES_SCHEMA,
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    from br_startup_mcp.tools.regulatory import (
        get_cvm_crowdfunding_offers,
        get_bndes_financing,
    )

    try:
        if name == "get_cvm_crowdfunding_offers":
            result = get_cvm_crowdfunding_offers(
                cnpj=arguments.get("cnpj"),
                status=arguments.get("status"),
                limit=int(arguments.get("limit", 20)),
            )
        elif name == "get_bndes_financing":
            result = get_bndes_financing(
                cnpj=arguments.get("cnpj"),
                produto=arguments.get("produto"),
                limit=int(arguments.get("limit", 20)),
            )
        else:
            result = json.dumps({"error": f"Unknown tool: {name}"})

        return [types.TextContent(type="text", text=result)]

    except Exception as e:
        error_msg = json.dumps(
            {"error": str(e), "tool": name}, ensure_ascii=False
        )
        return [types.TextContent(type="text", text=error_msg)]


async def main() -> None:
    """Entry point for the MCP server via stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
