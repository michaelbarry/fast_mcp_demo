# python ./quickstart_client.py
from fastmcp import Client
import asyncio

client = Client("quickstart_server.py")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

asyncio.run(call_tool("Mike"))