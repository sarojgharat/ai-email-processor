import asyncio
from typing import Optional
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session: Optional[ClientSession] = None
        self.tools = []
        self.client_context = None
        self.session_context = None
    
    async def connect(self):
        # Connect to the streamable HTTP server
        self.client_context = streamablehttp_client(self.server_url)
        read_stream, write_stream, _ = await self.client_context.__aenter__()
        # Create a session using the client streams
        self.session_context = ClientSession(read_stream, write_stream)
        self.session = await self.session_context.__aenter__()
        await self.session.initialize()
        resp = await self.session.list_tools()
        self.tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.inputSchema,
            }
            for t in resp.tools
        ]
        print("✅ Connected: Tools available =", [t["name"] for t in self.tools])
    

    async def close(self):
        if self.session_context:
            await self.session_context.__aexit__(None, None, None)
        if self.client_context:
            await self.client_context.__aexit__(None, None, None)

async def main():
    client = MCPClient("http://localhost:8004/mcp")
    try:
        await client.connect()
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())