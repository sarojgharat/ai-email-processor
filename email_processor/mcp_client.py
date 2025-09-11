import logging
from rich.logging import RichHandler

from typing import Any
from uuid import uuid4

import json
import httpx
import click
import asyncio

from db_client import create_email_request


from gmail_reader import GmailReaderService

# Configure logging to show INFO level messages
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)  # Get a logger instance


AGENT_URL="http://localhost:9999"
INITIAL_PROMPT = "What do you want to send to the agent? (type ':q' or 'quit' to exit)"

gmail_service = GmailReaderService("credentials.json")

async def invoke_agent(base_url, query, conversation_id) -> SendMessageResponse:
    





# -----------------------------------------------------------------------------
# @click.command(): Turns the function below into a command-line command
# -----------------------------------------------------------------------------
#@click.command()
#@click.option("--agent_url", default="http://localhost:10002", help="Base URL of the A2A agent server")
async def main():

    business_process = "booking"
    await read_and_process_emails(business_process, max_emails=2)

    business_process = "equipment"
    await read_and_process_emails(business_process, max_emails=2)


async def read_and_process_emails(business_process, max_emails):

    emails = gmail_service.read_emails(business_process, max_emails)
    for email in emails:
        conversation_id=uuid4().hex
        email_json = json.dumps(email, indent=4)
        payload = {
            "request_id": conversation_id,
            "business_process": business_process,
            "original_email": email
        }
        create_email_request(payload)
        payload_json = json.dumps(payload)
        logger.info(f"Request : {payload_json}")
        result = await invoke_agent(AGENT_URL, payload_json, conversation_id)
        agent_response = result.root.result.artifacts[0].parts[0].root.text
        logger.info(f"Response : {agent_response}")


if __name__ == '__main__': 
    asyncio.run(main())
