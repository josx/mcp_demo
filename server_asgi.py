import jwt
import datetime
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.types import Scope, Receive, Send
from starlette.exceptions import HTTPException
from server import mcp
from mcp.server.sse import SseServerTransport
from contextlib import asynccontextmanager


JWT_SECRET = "your-secret-key"

class JWTTransport(SseServerTransport):
    """
    Example jwt implementation of SSE server transport.
    """

    def authenticate(self, scope):
        auth_header = dict(scope["headers"]).get(b'authorization', b'')
        if not auth_header:
            return None
        token = auth_header.decode("utf-8").split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        print(payload)
        return payload


    @asynccontextmanager
    async def connect_sse(self, scope: Scope, receive: Receive, send: Send):
        if self.authenticate(scope):
            async with super().connect_sse(scope, receive, send) as streams:
                yield streams


async def welcome_message(request):
    return PlainTextResponse("Demo Mcp with jwt auth")


async def get_token(request):
    username = request.query_params.get("username", "demo_user")
    scope = request.query_params.get("scope", "mcp:access")
    token = jwt.encode({
        "username": username,
        "scope": scope,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm="HS256")
    return JSONResponse({"token": token})


# Create SSE transport
sse = JWTTransport("/messages/")

# MCP SSE handler function
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as (
        read_stream,
        write_stream,
    ):
        await mcp._mcp_server.run(
            read_stream, write_stream, mcp._mcp_server.create_initialization_options()
        )

routes = [
    Route("/", endpoint=welcome_message),
    Route("/get_token", get_token),
    Route("/sse", endpoint=handle_sse),
    Mount("/messages/", app=sse.handle_post_message),
]

app = Starlette(
            debug=True,
            routes=routes
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")
