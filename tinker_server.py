import httpx
from pydantic import BaseModel
from fastmcp import Context, FastMCP
from fastmcp.prompts import Message,UserMessage, AssistantMessage

# Create the MCP server
mcp = FastMCP("tinker")

# supporting classes
class UserInfo(BaseModel):
    user_id: int
    notify: bool = False


# context
# Gain access to MCP server capabilities within your tool or resource functions by adding a parameter type-hinted with fastmcp.Context.
@mcp.resource("system://status/{ctx}")
async def get_system_status(ctx: Context) -> dict:
    """Checks system status and logs information."""
    await ctx.info("Checking system status...")
    # Perform checks
    await ctx.report_progress(1, 1) # Report completion
    return {"status": "OK", "load": 0.5, "client": ctx.client_id}

# prompts
@mcp.prompt()
def ask_review(code_snippet: str) -> str:
    """Generates a standard code review request."""
    return f"Please review the following code snippet for potential bugs and style issues:\n```python\n{code_snippet}\n```"

@mcp.prompt()
def debug_session_start(error_message: str) -> list[Message]:
    """Initiates a debugging help session."""
    return [
        UserMessage(f"I encountered an error:\n{error_message}"),
        AssistantMessage("Okay, I can help with that. Can you provide the full traceback and tell me what you were trying to do?")
    ]



# tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.tool()
async def send_notification(user: UserInfo, message: str) -> dict:
    """Sends a notification to a user if requested."""
    if user.notify:
        # Simulate sending notification
        print(f"Notifying user {user.user_id}: {message}")
        return {"status": "sent", "user_id": user.user_id}
    return {"status": "skipped", "user_id": user.user_id}

@mcp.tool()
def get_stock_price(ticker: str) -> float:
    """Gets the current price for a stock ticker."""
    # Replace with actual API call
    prices = {"AAPL": 180.50, "GOOG": 140.20}
    return prices.get(ticker.upper(), 0.0)




# resource templates
# This is a resource template (dynamic resource)
@mcp.resource("db://users/{user_id}/email")
def get_user_email(user_id: str) -> str:
    """Retrieves the email address for a given user ID."""
    emails = {"123": "alice@example.com", "456": "bob@example.com"}
    return emails.get(user_id, "not_found@example.com")

@mcp.resource("config://app-version")
def get_app_version() -> str:
    """Returns the application version."""
    return "v2.1.0"

