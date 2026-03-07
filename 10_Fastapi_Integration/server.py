from fastmcp import FastMCP

mcp = FastMCP("AddServer")


@mcp.tool(description="Add two integers")
def add(a: int, b: int) -> int:
    return a + b
