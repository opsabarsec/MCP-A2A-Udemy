import http.client
import json

conn = http.client.HTTPConnection("127.0.0.1", 8000)

# First get a token from Auth0
auth0_conn = http.client.HTTPSConnection("dev-5rkk45hheaggb2vc.eu.auth0.com")

payload = '{"client_id":"nKBAc6jAhYg5Qw1hrMa31h29CsHXZaQk","client_secret":"1Sg7xy7EnVHTFQreF1TK9I9d9p4UNTO-D7dqYKuICYnGXMETX48-ZS8BNud1Nll0","audience":"http://127.0.0.1:8000/mcp","grant_type":"client_credentials"}'

headers = {"content-type": "application/json"}

auth0_conn.request("POST", "/oauth/token", payload, headers)

res = auth0_conn.getresponse()
data = res.read()
token_data = json.loads(data.decode("utf-8"))
access_token = token_data["access_token"]

print("Got token:", access_token[:50] + "...")

# Now make request to MCP server
mcp_headers = {
    "authorization": f"Bearer {access_token}",
    "content-type": "application/json",
}

mcp_payload = json.dumps(
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"},
        },
    }
)

conn.request("POST", "/mcp", mcp_payload, mcp_headers)

res = conn.getresponse()
data = res.read()

print("Response:", data.decode("utf-8"))
