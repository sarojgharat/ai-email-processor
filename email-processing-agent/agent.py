from google.adk.agents import Agent
from google.adk.tools import google_search

from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset


from dotenv import load_dotenv
import os
import logging
from rich.logging import RichHandler


load_dotenv()
# Create a logger for this module using its namespace
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)
SYSTEM_INSTRUCTION = os.getenv("SYSTEM_INSTRUCTION")

def get_mcp_tools():
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:8002/mcp'
            )
        ),
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:8004/mcp'
            )
        )
    ]
    return tools


root_agent = Agent (
        name="orchestraction_agent",
        model="gemini-2.5-pro",
        description="An agent that delegates to classification and data extraction task to other agents.",
        instruction=SYSTEM_INSTRUCTION,
        tools=get_mcp_tools(),
    )