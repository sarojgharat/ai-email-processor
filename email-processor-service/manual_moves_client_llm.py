import os
import getpass
import logging
import yaml
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.openapi import planner
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities.requests import RequestsWrapper
from langchain_community.tools.json.tool import JsonSpec

# Load environment variables from .env file
load_dotenv()

# --- Basic Setup ---
# Configure logging to see the agent's thought process
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set Google API Key securely
if not os.getenv("GOOGLE_API_KEY"):
    try:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")
    except Exception as e:
        logger.error(f"Could not read API key: {e}")
        exit()


class ManualMovesClientLLM:
    """
    An LLM client to interact with the Manual Moves API.
    """

    def __init__(self):
        """
        Initializes the client, the language model, and the OpenAPI agent.
        """
        # 1. Load and reduce the OpenAPI specification
        with open("shipping-manual-moves-api-specs.yaml") as f:
            raw_openai_api_spec = yaml.load(f, Loader=yaml.Loader)
        openai_api_spec = reduce_openapi_spec(raw_openai_api_spec)

        ALLOW_DANGEROUS_REQUEST = True  # Set to True if you want to allow POST/PUT/DELETE requests
        
        # 2. Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

        # 3. Create a requests wrapper for making HTTP calls
        requests_wrapper = RequestsWrapper()

        # 4. Create the OpenAPI toolkit from the specification
        agent = planner.create_openapi_agent(
            openai_api_spec,
            requests_wrapper,
            llm,
            allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
        )
        self.agent = agent

    def create_manual_move(self, text: str) -> None:
        """
        Uses the agent to process a natural language command and interact with the API.

        Args:
            text: The user's command as a string.
        """
        logger.info(f"Received input text: '{text}'")
        
        # The .run() method is deprecated. Use .invoke() instead.
        # The input must be a dictionary with the key "input".
        try:
            response = self.agent.invoke({"input": text})
            logger.info(f"Agent response: {response.get('output', 'No output found.')}")
        except Exception as e:
            logger.error(f"An error occurred while running the agent: {e}")


if __name__ == "__main__":
    client = ManualMovesClientLLM()
    client.create_manual_move(
        "Create a new manual move from Warehouse A to Warehouse B for equipment EQP-4567 by John Doe"
    )

