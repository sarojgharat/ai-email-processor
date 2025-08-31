# utilities/discovery.py
# =============================================================================
# 🎯 Purpose:
# A shared utility module for discovering Agent-to-Agent (A2A) servers.
# It reads a registry of agent base URLs (from a JSON file) and fetches
# each agent's metadata (AgentCard) from the standard discovery endpoint.
# This allows any client or agent to dynamically learn about available agents.
# =============================================================================

import os                            # os provides functions for interacting with the operating system, such as file paths
import json                          # json allows encoding and decoding JSON data
import logging                       # logging is used to record warning/error/info messages
from rich.logging import RichHandler
from typing import List             # List is a type hint for functions that return lists

import httpx                         # httpx is an async HTTP client library for sending requests
from a2a.types import AgentCard
from a2a.client import A2ACardResolver


# Create a named logger for this module; __name__ is the module's name
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


class DiscoveryClient:
    """
    🔍 Discovers A2A agents by reading a registry file of URLs and querying
    each one's /.well-known/agent.json endpoint to retrieve an AgentCard.

    Attributes:
        registry_file (str): Path to the JSON file listing base URLs (strings).
        base_urls (List[str]): Loaded list of agent base URLs.
    """

    def __init__(self, registry_file: str = None):
        """
        Initialize the DiscoveryClient.

        Args:
            registry_file (str, optional): Path to the registry JSON. If None,
                defaults to 'agent_registry.json' in this utilities folder.
        """
        # If the caller provided a custom path, use it; otherwise, build the default path
        if registry_file:
            self.registry_file = registry_file
        else:
            # __file__ is this module's file; dirname gets the folder containing it
            # join constructs a path to 'agent_registry.json' alongside this script
            self.registry_file = os.path.join(
                os.path.dirname(__file__),
                "agent_registry.json"
            )

        # Immediately load the registry file into memory
        self.base_urls = self._load_registry()

    def _load_registry(self) -> List[str]:
        """
        Load and parse the registry JSON file into a list of URLs.

        Returns:
            List[str]: The list of agent base URLs, or empty list on error.
        """
        try:
            # Open the file at self.registry_file in read mode
            with open(self.registry_file, "r") as f:
                # Parse the entire file as JSON
                data = json.load(f)
            # Ensure the JSON is a list, not an object or other type
            if not isinstance(data, list):
                raise ValueError("Registry file must contain a JSON list of URLs.")
            return data
        except FileNotFoundError as e:
            # If the file doesn't exist, log a warning and return an empty list
            logger.warning(f"Registry file not found: {self.registry_file}, {e}")
            return []
        except (json.JSONDecodeError, ValueError) as e:
            # If JSON is invalid or wrong type, log an error and return empty list
            logger.error(f"Error parsing registry file: {e}")
            return []

    async def list_agent_cards(self) -> List[AgentCard]:
        """
        Asynchronously fetch the discovery endpoint from each registered URL
        and parse the returned JSON into AgentCard objects.

        Returns:
            List[AgentCard]: Successfully retrieved agent cards.
        """
        cards: List[AgentCard] = []  # Prepare an empty list to collect AgentCard instances

        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as httpx_client:
            # Iterate through each base URL in the registry
            for url in self.base_urls:
                try:
                    # Initialize A2ACardResolver
                    resolver = A2ACardResolver(
                        httpx_client=httpx_client,
                        base_url=url,
                        # agent_card_path uses default, extended_agent_card_path also uses default
                    )
                    card = await resolver.get_agent_card()
                    cards.append(card)
                except Exception as e:
                    # If anything goes wrong, log which URL failed and why
                    logger.warning(f"Failed to discover agent at {url}: {e}")

        return cards                    