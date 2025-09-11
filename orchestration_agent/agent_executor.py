# =============================================================================
# agents/host_agent/agent_executor.py
# =============================================================================
# Purpose:
# This file defines the "executor" that acts as a bridge between the A2A server
# and the underlying Orchestration agent. It listens to tasks and 
# dispatches them to the agent, then sends back task updates and results 
# through the event queue.
# =============================================================================

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

from agent import OrchestrationAgent  # Imports the OrchestrationAgent class from the same directory

# Importing base classes from the A2A SDK to define agent behavior
from a2a.server.agent_execution import AgentExecutor  # Base class for defining agent task executor logic
from a2a.server.agent_execution import RequestContext  # Holds information about the incoming user query and context

# EventQueue is used to push updates back to the A2A server (e.g., task status, results)
from a2a.server.events.event_queue import EventQueue
from google.genai import types


import json



# Importing event and status types for responding to client
from a2a.types import (
    TaskState,               # Enum that defines states: working, completed, input_required, etc.
    TextPart,
    Part
)
from a2a.types import (
    AgentCard
)

from a2a.server.tasks import TaskUpdater

# Utility functions to create standardized message and artifact formats
from a2a.utils import (
    new_task,                # Creates a new task object from the initial message
)


# -----------------------------------------------------------------------------
# OrchestrationAgentExecutor: Connects the agent logic to A2A server infrastructure
# -----------------------------------------------------------------------------
class OrchestrationAgentExecutor(AgentExecutor):
    """
    This class connects the OrchestrationAgent to the A2A server runtime. It implements
    the `execute` function to run tasks and push updates to the event queue.
    """

    def __init__(self):
        self.agent = OrchestrationAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        # This method is called when a new task is received

        query = context.get_user_input()  # Extracts the actual text of the user's message
        task = context.current_task      # Gets the task object if it already exists

        if not context.message:          # Ensure the message is not missing
            raise Exception('No message provided')  # Raise an error if something's wrong

        if not task:                     # If no existing task, this is a new interaction
            task = new_task(context.message)       # Create a new task based on the message
            await event_queue.enqueue_event(task)        # Enqueue the new task to notify the A2A server

        task_updater = TaskUpdater(event_queue, context.task_id, context.context_id)            
        if not context.current_task:
            await task_updater.submit()

        await task_updater.start_work()

        await self.process_request(query, task.context_id, task_updater)

    
    async def process_request(self, query, context_id, task_updater):
        # Use the agent to handle the query via async stream
        async for event in self.agent.invoke_agent(query, "saroj", context_id):

            if event['is_task_complete']:  # If the task has been successfully completed
                # Send the result artifact to the A2A server
                await task_updater.add_artifact([Part(root=TextPart(text=event['content']) )])
                # Send final status update: task is completed
                await task_updater.complete()
                break

            elif event['require_user_input']:  # If the agent needs more information from user
                # Enqueue an input_required status with a message
                await task_updater.update_status(
                    TaskState.input_required,
                    message=task_updater.new_agent_message([Part(root=TextPart(text=event['content']) )])
                )

            else:  # The task is still being processed (working)
                # Enqueue a status update showing ongoing work
                await task_updater.update_status(
                    TaskState.working,
                    message=task_updater.new_agent_message([Part(root=TextPart(text=event['content']) )])
                )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        # Optional method to cancel long-running tasks (not supported here)
        raise Exception('Cancel not supported')  # Raise error since this agent doesn’t support canceling