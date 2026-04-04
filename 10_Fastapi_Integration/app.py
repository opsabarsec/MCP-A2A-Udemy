import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from server import mcp

mcp_app = mcp.http_app(path="/mcp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp_app.lifespan(app):
        yield


app = FastAPI(lifespan=lifespan)

app.mount("/mcpserver", mcp_app)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
