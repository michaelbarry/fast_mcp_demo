import asyncio
import logging
import sys
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("fastmcp_client")

server_script = "tinker_server.py"

async def use_stdio_client_inferred():
    logger.info(f"Creating client with inferred transport for {server_script}")
    client = Client(server_script)
    
    try:
        logger.info("Connecting to server with inferred transport...")
        async with client:
            logger.info(f"Connected: {client.is_connected()}")
            
            logger.info("Listing tools...")
            tools = await client.list_tools()
            logger.info(f"Found tools: {tools}")
            
            # Try other operations if available
            if any(tool.name == "greet" for tool in tools):
                logger.info("Calling 'greet' tool...")
                result = await client.call_tool("greet", {"name": "World"})
                logger.info(f"Greet result: {result}")
    except Exception as e:
        logger.error(f"Error with inferred transport: {e}", exc_info=True)

async def use_stdio_client_explicit():
    logger.info(f"Creating explicit PythonStdioTransport for {server_script}")
    transport = PythonStdioTransport(
        script_path=server_script,
        python_cmd="python3",  # Use default python or specify path
        # args=["--some-server-arg"],  # Uncomment if needed
        # env={"MY_VAR": "value"},     # Uncomment if needed
    )
    
    logger.info("Creating client with explicit transport")
    client = Client(transport)
    
    try:
        logger.info("Connecting to server with explicit transport...")
        async with client:
            logger.info(f"Connected: {client.is_connected()}")
            
            logger.info("Listing tools...")
            tools = await client.list_tools()
            logger.info(f"Found tools: {tools}")
            
            # Try other operations if available
            if any(tool.name == "greet" for tool in tools):
                logger.info("Calling 'greet' tool...")
                result = await client.call_tool("greet", {"name": "World"})
                logger.info(f"Greet result: {result}")
    except Exception as e:
        logger.error(f"Error with explicit transport: {e}", exc_info=True)

async def main():
    logger.info("Starting client test script")
    
    # Try both methods
    logger.info("Testing inferred transport...")
    await use_stdio_client_inferred()
    
    logger.info("Testing explicit transport...")
    await use_stdio_client_explicit()
    
    logger.info("Client test script completed")

if __name__ == "__main__":
    # This is important - you need to actually run the async functions!
    asyncio.run(main())