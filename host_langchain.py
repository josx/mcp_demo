import asyncio
import sys
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama


async def main(model: str, base_url: str):
    model = ChatOllama(model=model, base_url=base_url)
    client = MultiServerMCPClient({
        "demo_server": {
            "url": "http://localhost:8000/sse",
            "transport": "sse",
        }
    })
    agent = create_react_agent(model, client.get_tools())
    response = await agent.ainvoke({
        "messages": "which universities are in argentina?"
    })
    print(response)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        filename = os.path.basename(__file__)
        print("Usage: python {} <model> <ollama_base_url>".format(filename))
        print(
            "Example: python {} llama3.3 http://localhost:11434"
            .format(filename)
        )
        sys.exit(1)

    asyncio.run(main(sys.argv[1], sys.argv[2]))
