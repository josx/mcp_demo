# Demo MCP

## Info
- Server - Using server examples from [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- Client - Using code from [slavashvets/mcp-http-client-example](https://github.com/slavashvets/mcp-http-client-example/)
- Debug -  Using [Inspector](https://github.com/modelcontextprotocol/inspector)


## Setup
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run Server
- `python server.py`


## Run demo client
- `python client.py http://localhost:8000/sse`


## Debug
- Open a new terminal and run `npx @modelcontextprotocol/inspector`
- Point browser to http://127.0.0.1:6274 
- Change Transport Type to `SSE`
- Change URL to `http://localhost:8000/sse`
- Press `Connect` and start testing server
