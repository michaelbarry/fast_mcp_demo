import asyncio
from fastmcp import Client

async def main():
    print(f"attempting to connect to server...")
    
    # Create and connect to the client within the async with block
    async with Client("tinker_server.py") as client:
        print(f"connected to server")
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")

        if any(tool.name == "greet" for tool in tools):
            result = await client.call_tool("greet", {"name": "World"})
            print(f"Greet result: {result}")

    # Connection is closed automatically here
    print(f"Client disconnected")

if __name__ == "__main__":
    asyncio.run(main())