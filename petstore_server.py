import asyncio
import httpx
from fastmcp import FastMCP

# Import the OpenAPI spec from the separate file
from petstore_spec import PETSTORE_SPEC

def main():
    # Create HTTP client pointing to our local server
    client = httpx.AsyncClient(base_url="http://localhost:5000")
    
    # Create the MCP server with our imported spec - notice the missing "await"
    # FastMCP.from_openapi is a synchronous method in this version
    mcp = FastMCP.from_openapi(
        openapi_spec=PETSTORE_SPEC,
        client=client,
        name="PetStore"
    )
    
    # Define an async function to get the components
    async def get_components():
        # Use get_ methods instead of list_ methods
        tools = await mcp.get_tools()
        resources = await mcp.get_resources()
        templates = await mcp.get_resource_templates()
        
        print(f"Tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool}")
            
        print(f"Resources: {len(resources)}")
        for resource in resources:
            print(f"  - {resource}")
            
        print(f"Templates: {len(templates)}")
        for template in templates:
            print(f"  - {template}")
    
    # Run the async function to get components
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_components())
    
    # Start the MCP server (this is synchronous)
    print("\nStarting FastMCP server...")
    mcp.run()

if __name__ == "__main__":
    print("Pet Store FastMCP Client")
    print("Make sure the petstore_server.py is running first!")
    main()  # Call regular main, not asyncio.run(main())