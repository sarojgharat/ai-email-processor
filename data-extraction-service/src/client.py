from mcp import ClientSession
from mcp.client.sse import sse_client


async def run():
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(tools)

             # Call a tool
            result = await session.call_tool("extract_data", arguments=
                                             {"process": "booking", "category" : "booking amendment" ,"input_text": "This request is for new booking"})
            print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
