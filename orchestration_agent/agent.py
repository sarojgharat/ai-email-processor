from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams


from google.genai import types
from datetime import datetime
from typing import Optional
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from typing import Any, Literal, AsyncIterable
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Task
)

import httpx
import json
import uuid
from a2a.client import A2ACardResolver
from remote_agent_connector import RemoteAgentConnector
import vertexai
from vertexai.preview.prompts import Prompt
from vertexai.preview import prompts

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


# -----------------------------------------------------------------------------
# OrchestrationAgent Class Definition
# -----------------------------------------------------------------------------
class OrchestrationAgent:
    """
    Google ADK agent that identifies the intent of the request
    - Reads email and idetifies business process
    - Classifies the request into predefined categories as per the business process.
    - Extracts data from the email into JSON format as per the business process.
    - Powered by Gemini Flash model
    """

    # Instruction given to the agent LLM
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))
    prompt = prompts.get(os.getenv("SYSTEM_INSTRUCTION_ID"))
    SYSTEM_INSTRUCTION = prompt.system_instruction if prompt.system_instruction else os.getenv("SYSTEM_INSTRUCTION")

    def __init__(self) -> None:
        self.agent = self.build_agent()
        # ADK runner = orchestrates the agent execution
        self.runner = Runner(
            app_name=self.agent.name,
            agent=self.agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )



    def build_agent(self) -> Agent:

        orchestraction_agent = Agent (
                name="orchestraction_agent",
                model="gemini-2.5-pro",
                description="An agent that delegates to classification and data extraction task to other agents.",
                instruction=self.SYSTEM_INSTRUCTION,
                tools=[
                    MCPToolset(
                        connection_params=SseConnectionParams(
                            url="http://localhost:8000/sse"  # Replace with your MCP server URL
                        )
                    ),
                    MCPToolset(
                        connection_params=SseConnectionParams(
                            url="http://localhost:8001/sse"  # Replace with your MCP server URL
                        )
                    )
                ],
            )
    
        return orchestraction_agent
    
    # Define an asynchronous method that returns an iterable (like a loop) of dictionaries.
    # Each dictionary is a partial update from the agent.
    async def invoke_agent(self, query, user_id, context_id) -> AsyncIterable[dict[str, Any]]:

        content = types.Content(role='user', parts=[types.Part(text=query)])
        logger.info(f"Orchestration Agent Request: {content}")

        session_id = await self.upsert_session(user_id, context_id)
        
        events = self.runner.run_async(user_id=user_id, session_id=session_id, new_message=content)

        async for event in events:
            #logger.info(f"*****************************: {event}")
            if event.is_final_response():
                logger.info(f"Orchestration Agent Response (Final): {event}")
                yield {
                    "is_task_complete": True,             # Not done yet
                    "require_user_input": False,            # Ask the user to clarify
                    "content": event.content.parts[0].text,         # The question or error to show
                }
            #elif event.is_input_required():
            #    logger.info(f"Orchestration Agent Response (More Input required): {event}")
            #    yield {
            #        "is_task_complete": False,             # Not done yet
            #        "require_user_input": True,            # Ask the user to clarify
            #        "content": event.content.parts[0].text,         # The question or error to show
            #    }
            elif calls := event.get_function_calls():
                #logger.info(f"Orchestration Agent Response (Tool Calls): {calls}")
                yield {  # Yield means "send this result immediately" before continuing
                    "is_task_complete": False,         # Not done yet
                    "require_user_input": False,       # No follow-up question to the user (yet)
                    "content": "Calling Tools for processing email",  # What to display on the UI or CLI
                }
            else:
                #logger.info(f"Orchestration Agent Response (Intermediate Update): {event}")
                yield {  # Yield means "send this result immediately" before continuing
                    "is_task_complete": False,         # Not done yet
                    "require_user_input": False,       # No follow-up question to the user (yet)
                    "content": "Processing the email",  # What to display on the UI or CLI
                }

    async def upsert_session(self, user_id, context_id: str):
        session = await self.runner.session_service.get_session(
            app_name=self.runner.app_name, user_id=user_id, session_id=context_id
        )
        if session is None:
            session = await self.runner.session_service.create_session(
                app_name=self.runner.app_name,
                user_id=user_id,
                session_id=context_id,
            )
        if session is None:
            raise RuntimeError(f"Failed to get or create session: {context_id}")
        return session.id