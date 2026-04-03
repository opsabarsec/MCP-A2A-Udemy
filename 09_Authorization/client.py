import asyncio
import os

import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
API_AUDIENCE = os.getenv("API_AUDIENCE", "http://127.0.0.1:8000/mcp")


async def get_auth0_token() -> str:
    """
    Request an access token from Auth0 using the Client Credentials Grant.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    print(token_url)
    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": API_AUDIENCE,
        "scope": "read:add",
    }
    async with httpx.AsyncClient() as http:
        response = await http.post(token_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["access_token"]


async def main():
    token = await get_auth0_token()
    print("Got Auth0 token:", token)

    transport = StreamableHttpTransport(
        url=API_AUDIENCE, headers={"Authorization": f"Bearer {token}"}
    )

    client = Client(transport)
    async with client:
        result = await client.call_tool("add", {"a": 5, "b": 7})

        # pre-v2.10: result was a list of Content objects, so we accessed the first item.
        # print("5 + 7 =", result[0].text)

        # v2.10+: result is a single CallToolResult object.
        print("5 + 7 =", result.data)


if __name__ == "__main__":
    asyncio.run(main())
