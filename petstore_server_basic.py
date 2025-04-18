# % fastmcp dev ./petstore_server_basic.py
import httpx
from fastmcp import FastMCP
from petstore_spec import PETSTORE_SPEC as spec

# Create a client for your API
api_client = httpx.AsyncClient(base_url="http://localhost:5000")


# Create an MCP server from your OpenAPI spec
mcp = FastMCP.from_openapi(openapi_spec=spec, client=api_client)

if __name__ == "__main__":
    mcp.run()