"""MCP HTTP client example using MCP SDK."""
import os
import asyncio
import sys
import requests
from typing import Any
from urllib.parse import urlparse

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


def print_items(name: str, result: Any) -> None:
    """Print items with formatting.

    Args:
        name: Category name (tools/resources/prompts)
        result: Result object containing items list
    """
    print("", f"Available {name}:", sep="\n")
    items = getattr(result, name)
    if items:
        for item in items:
            print(" *", item)
    else:
        print("No items available")


async def main(server_url: str, headers: dict[str, Any] | None = None):
    """Connect to MCP server and list its capabilities.

    Args:
        server_url: Full URL to SSE endpoint (e.g. http://localhost:8000/sse)
    """

    try:
        async with sse_client(server_url, headers) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                print("Connected to MCP server at", server_url)
                print_items("tools", (await session.list_tools()))
                print_items("resources", (await session.list_resources()))
                print_items("resourceTemplates", (
                    await session.list_resource_templates())
                )
                print_items("prompts", (await session.list_prompts()))

                add_result = await session.call_tool(
                    "add", arguments={"a": 1, "b": 2}
                )
                print_items("content", add_result)

                fecth_result = await session.call_tool(
                    "fetch_u", arguments={"country": "Argentina"}
                )
                print_items("content", fecth_result)

                echo_result = await session.call_tool(
                    "echo_tool", arguments={"message": "DEMO"}
                )
                print_items("content", echo_result)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        filename = os.path.basename(__file__)
        print("Usage: python {} <server_url>".format(filename))
        print("Example: python {} http://localhost:8000/sse".format(filename))
        sys.exit(1)

    urlparsed = urlparse(sys.argv[1])
    if urlparsed.scheme not in ("http", "https"):
        print("Error: Server URL must start with http:// or https://")
        sys.exit(1)

    headers = {}
    try:
        r = requests.get(
            urlparsed.scheme + '://' + urlparsed.netloc + '/get_token'
        )
        json_response = r.json()
        headers['Authorization'] = "Bearer " + json_response["token"]
    except Exception:
        print("Can not use auth endpoint")

    asyncio.run(main(sys.argv[1], headers))
