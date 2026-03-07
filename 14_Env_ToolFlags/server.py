import os
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(name="SimpleDemo")


def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return a - b


if os.getenv("MCP_TOOL_ADD") == "True":
    mcp.tool(add)

if os.getenv("MCP_TOOL_SUBTRACT") == "True":
    mcp.tool(subtract)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1")
