import logging
from rich.logging import RichHandler

from typing import Any
from uuid import uuid4

import json
import httpx
import click
import asyncio

from db_client import create_email_request

from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse
)

from a2a.client import A2ACardResolver, A2AClient

from a2a.utils.constants import (
    AGENT_CARD_WELL_KNOWN_PATH,
    EXTENDED_AGENT_CARD_PATH,
)

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
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as httpx_client:
        
        try:
            # Initialize A2ACardResolver
            resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=base_url
            )

            public_card = await resolver.get_agent_card()
            response = await trigger_agent(httpx_client, public_card, query, conversation_id)

        except Exception as e:
            logger.error(
                f'Critical error fetching public agent card: {e}', exc_info=True
            )
            raise RuntimeError(
                'Failed to fetch the public agent card. Cannot continue.'
            ) from e


        return response


async def trigger_agent(httpx_client, final_agent_card_to_use, query, conversation_id) -> SendMessageResponse:
    
    client = A2AClient(
            httpx_client=httpx_client, agent_card=final_agent_card_to_use
        )
    
    parts = [{'kind': 'text', 'text': query}]
    send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': parts,
                'messageId': uuid4().hex,
                'contextId': conversation_id
            },
        }
    
    
    request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )

    request_json = request.model_dump(mode='json', exclude_none=True)
    logger.info(f"Client Request : {json.dumps(request_json, indent=4)}" )

    response = await client.send_message(request)
    response_json = response.model_dump(mode='json', exclude_none=True)
    logger.info(f"Client Response : {json.dumps(response_json, indent=4)}")

    return response


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
