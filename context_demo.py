from fastmcp import FastMCP, Context

mcp = FastMCP(name="ContextDemo")


@mcp.tool()
async def show_files() -> list[str]:
    """Lists all files in the current directory."""
    import os
    files = os.listdir(".")
    return files


@mcp.tool()
async def process_file(file_uri: str, ctx: Context) -> str:
    """Processes a file, using context for logging and resource access."""
    request_id = ctx.request_id
    await ctx.info(f"[{request_id}] Starting processing for {file_uri}")

    try:
        # Use context to read a resource
        contents_list = await ctx.read_resource(file_uri)
        if not contents_list:
            await ctx.warning(f"Resource {file_uri} is empty.")
            return "Resource empty"

        data = contents_list[0].content # Assuming TextResourceContents
        await ctx.debug(f"Read {len(data)} bytes from {file_uri}")

        # Report progress
        await ctx.report_progress(progress=50, total=100)
        
        # Simulate work
        processed_data = data.upper() # Example processing

        await ctx.report_progress(progress=100, total=100)
        await ctx.info(f"Processing complete for {file_uri}")

        return f"Processed data length: {len(processed_data)}"

    except Exception as e:
        # Use context to log errors
        await ctx.error(f"Error processing {file_uri}: {str(e)}")
        raise # Re-raise to send error back to client


@mcp.tool()
async def analyze_data(data: list[float], ctx: Context) -> dict:
    """Analyze numerical data with logging."""
    await ctx.debug("Starting analysis of numerical data")
    await ctx.info(f"Analyzing {len(data)} data points")
    
    try:
        result = sum(data) / len(data)
        await ctx.info(f"Analysis complete, average: {result}")
        return {"average": result, "count": len(data)}
    except ZeroDivisionError:
        await ctx.warning("Empty data list provided")
        return {"error": "Empty data list"}
    except Exception as e:
        await ctx.error(f"Analysis failed: {str(e)}")
        raise

@mcp.resource("document://sample")
def get_sample_document() -> str:
    return "This is a sample document with some text content that can be summarized."


@mcp.resource("document://hello")
def get_sample_document() -> str:
    return open("./hello.txt", "r").read(-1)
    # return "This is a sample document with some text content that can be summarized."


@mcp.tool()
async def summarize_document(document_uri: str, ctx: Context) -> str:    
    """Summarize a document by its resource URI.
    example: document://sample
    This function reads the document content and generates a summary.
    """
    
    # Example document URI
    # document_uri = "document://sample"

    # Read the document content
    content_list = await ctx.read_resource(document_uri)
    
    if not content_list:
        return "Document is empty"
    
    document_text = content_list[0].content
    
    # Example: Generate a simple summary (length-based)
    words = document_text.split()
    total_words = len(words)
    
    await ctx.info(f"Document has {total_words} words")
    
    # Return a simple summary
    if total_words > 100:
        summary = " ".join(words[:100]) + "..."
        return f"Summary ({total_words} words total): {summary}"
    else:
        return f"Full document ({total_words} words): {document_text}"
    

@mcp.tool()
async def analyze_sentiment(text: str, ctx: Context) -> dict:
    """Analyze the sentiment of a text using the client's LLM."""
    # Create a sampling prompt asking for sentiment analysis
    prompt = f"Analyze the sentiment of the following text as positive, negative, or neutral. Just output a single word - 'positive', 'negative', or 'neutral'. Text to analyze: {text}"
    
    # Send the sampling request to the client's LLM
    response = await ctx.sample(prompt)
    
    # Process the LLM's response
    sentiment = response.text.strip().lower()
    
    # Map to standard sentiment values
    if "positive" in sentiment:
        sentiment = "positive"
    elif "negative" in sentiment:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {"text": text, "sentiment": sentiment}



@mcp.tool()
async def request_info(ctx: Context) -> dict:
    """Return information about the current request."""
    return {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id or "Unknown client"
    }


@mcp.tool()
async def advanced_tool(ctx: Context) -> str:
    """Demonstrate advanced context access."""
    # Access the FastMCP server instance
    server_name = ctx.fastmcp.name
    
    # Low-level session access (rarely needed)
    session = ctx.session
    request_context = ctx.request_context
    
    return f"Server: {server_name}"