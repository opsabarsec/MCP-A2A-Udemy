import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

SERVER = "http://127.0.0.1:3000/mcp/"


def section(title: str):
    print(f"\n{'=' * 10} {title} {'=' * 10}")


async def main() -> None:
    async with Client(StreamableHttpTransport(SERVER)) as session:
        tools = await session.list_tools()
        section("Available Tools")
        for tool in tools:
            print(f"Tool Name: {tool.name}")

        resources = await session.list_resources()
        section("Available Resources")
        for res in resources:
            print(f"Resource Name: {res.name}    URI: {res.uri}")

        # v3.0+: all routes are tools by default, use actual generated tool names
        tool_names = [t.name for t in tools]
        list_tool = next(t for t in tool_names if "list_products" in t)
        create_tool = next(t for t in tool_names if "create_product" in t)

        section("All Products (Before)")
        all_products = await session.call_tool(list_tool, {})
        print("Products:", all_products.data)

        section(f"Calling Tool: {create_tool}")
        created = await session.call_tool(
            create_tool,
            {"name": "Widget", "price": 19.99},
        )
        print("Created product:", created.data)

        section("All Products (After)")
        updated_products = await session.call_tool(list_tool, {})
        print("Products:", updated_products.data)


if __name__ == "__main__":
    asyncio.run(main())
