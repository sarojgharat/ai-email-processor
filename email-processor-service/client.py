import logging
from rich.logging import RichHandler

from typing import Any
from uuid import uuid4

import requests
import json

from manual_moves_client_llm import ManualMovesClientLLM

from db_client import create_email_request, update_email_request, get_email_request, get_all_emails, delete_email_request


# Configure logging to show INFO level messages
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)  # Get a logger instance

def main():

    all_emails = get_all_emails()
    print(all_emails)
    
    for email in all_emails:    
        print(email)

        if email['processingStatus'] == "PENDING":
            print(f"Processing email ID: {email['id']}")
            input_text_payload = {
                "from": email['from'],
                "subject": email['subject'],
                "body": email['body']
            }

            input_text = json.dumps(input_text_payload)
            classification = classify_text(
                process=email['businessProcess'],
                text=input_text
            )
            print("Classification Result:=================", classification)
            update_payload = {
                "classification_type": classification['classification_type'],
            }
            update_email_request(email['id'], update_payload)

            extracted_data = extract_data(
                process=email['businessProcess'],
                category=classification['classification_type'],
                text=input_text
            )
            print("Extraction Result:=====================", extracted_data)
            update_payload = {
                "extracted_data": sanitize(extracted_data.get('extracted_data', {})),
            }
            update_email_request(email['id'], update_payload)

            invocation_status = trigger_automation(classification['classification_type'], extracted_data.get('extracted_data', {}))            
            if invocation_status:
                update_payload = {
                    "automation_status": "TRIGGERED",
                    "processing_status": "PROCESSED"
                }
                update_email_request(email['id'], update_payload)

def trigger_automation(classification_type: str, extracted_data: str):
    invocation_status = False
    if classification_type == "manual move request":
        print("Triggering manual move request automation...")
        client = ManualMovesClientLLM()
        client.create_manual_move(
            extracted_data
        )
        invocation_status = True
    return invocation_status


def sanitize(data: str) -> str:
    data = data.replace("```json", "")
    data = data.replace("```", "")
    print("Sanitized Data: ", data)
    json_data = json.loads(data)
    return json_data

def classify_text(process: str, text: str):
    url = "http://localhost:8001/classify"
    payload = {
        "process": process,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e}")
        return None

def extract_data(process: str, category: str, text: str):
    url = "http://localhost:8003/extract"
    payload = {
        "process": process,
        "category": category,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with API: {e} traceback {e.__traceback__}")
        return None
    

if __name__ == '__main__': 
    main()
