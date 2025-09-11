import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill
)
from agent_executor import OrchestrationAgentExecutor
from utilities.discovery_client import DiscoveryClient

import click
import asyncio 
import logging
from rich.logging import RichHandler

from dotenv import load_dotenv

load_dotenv()

# Configure root logger to show INFO-level messages
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)

@click.command()
@click.option('--host', 'host', default='localhost')     # Host where the agent will listen (default: localhost)
@click.option('--port', 'port', default=9999)            # Port where the agent will listen (default: 9999)
@click.option(
    "--registry",
    default="utilities/agent_registry.json",
    help=(
        "Path to JSON file listing child-agent URLs. "
        "Defaults to agent_registry.json"
    )
)
def main(host: str, port: int, registry: str):

    # 1) Discover all registered child agents from the registry file
    discovery = DiscoveryClient(registry_file=registry)
    # Run the async discovery synchronously at startup
    agent_cards = asyncio.run(discovery.list_agent_cards())

    # Warn if no agents are found in the registry
    if not agent_cards:
        logger.warning(
            "No agents found in registry – the orchestrator will have nothing to call"
        )

    skill = AgentSkill(
        id='orchestrate_agents',
        name='Skills for Orchestrate request across available agents',
        description='A skill that reads email and delegates task to other agents to classify email and extract data in json format.',
        tags=['email processor', 'orchestrate'],
        examples=['Read email from booking folder and classify and extract data from email']
    )
    
    agent_card = AgentCard(
        name='Orchestration Agent',
        description='An agent that reads email and delegates task to other agents to classify email and extract data in json format.',
         url=f"http://{host}:{port}/",
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill]
    )

    request_handler = DefaultRequestHandler(
        agent_executor=OrchestrationAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    uvicorn.run(server.build(), host=host, port=port)

if __name__ == '__main__':
    main()