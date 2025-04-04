# server.py
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# tools
@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
async def fetch_u(country: str) -> str:
    """Fetch university for a country"""
    URL = "http://universities.hipolabs.com/search?country="
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL}{country}")
        return response.text


# resources
# Dynamic
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Static
@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"


# prompts
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


mcp.run(transport="sse")
