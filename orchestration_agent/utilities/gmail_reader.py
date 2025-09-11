from google.adk.agents import Agent
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
   # Authenticate the user
    creds = None
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)


    # Connect to Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service

def read_latest_email() -> dict:
    try:
        service = get_gmail_service()
        label_id = get_label_id(service, 'booking')

        results = service.users().messages().list(userId='me', labelIds=[label_id], maxResults=1).execute()
        messages = results.get('messages', [])
        if not messages:
            return {"status": "error", "error_message": "No emails found."}
        msg_id = messages[0]['id']
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        subject = headers.get('Subject', '')
        from_email = headers.get('From', '')
        to_email = headers.get('To', '')
        date = headers.get('Date', '')
        # Get body (plain text)
        body = ""
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    import base64
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        else:
            body = msg['payload']['body'].get('data', '')
            if body:
                import base64
                body = base64.urlsafe_b64decode(body).decode('utf-8')
        return {
            "status": "success",
            "email": {
                "subject": subject,
                "from": from_email,
                "to": to_email,
                "date": date,
                "body": body,
                "metadata": headers
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def get_label_id(service, label_name):
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])  
        for label in labels:
            if label['name'].lower() == label_name.lower():
                return label['id']
        return None
    except Exception as e:
        print(f"Error retrieving label ID: {str(e)}")
        return None
    
def main():
    email_data = read_latest_email()
    print(email_data)

if __name__ == '__main__':
    main()