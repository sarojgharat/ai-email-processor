from google.adk.agents import Agent
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.header import decode_header
import base64
import os
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailReaderService:

    def __init__(self, credentials_file, token_file='token.json'):
        creds = None

        # Load existing token if available
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)

        # If no valid credentials, do login and save token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for next time
            with open(token_file, 'w') as token:
                token.write(creds.to_json())




        # Connect to Gmail API
        self.service = build('gmail', 'v1', credentials=creds)
        

    def read_emails(self, label: str, max_count: int) -> dict:
        emails = []
        try:
            label_id = self.get_label_id(self.service, label)

            results = self.service.users().messages().list(userId='me', labelIds=[label_id], maxResults=max_count).execute()
            messages = results.get('messages', [])
            
            for message in messages:
                email = self.extract_email(message, label)
                emails.append(email)
            
        except Exception as e:
            print (e)
            #return {"status": "error", "error_message": str(e)}
        
        return emails

    def extract_email(self, message, label):
        msg_id = message['id']
        msg = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
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
                    #body = self.decode_mime_header(base64.urlsafe_b64decode(part['body']['data']))
                    break
        else:
            body = msg['payload']['body'].get('data', '')
            if body:
                import base64
                body = base64.urlsafe_b64decode(body).decode('utf-8')
                #body = self.decode_mime_header(base64.urlsafe_b64decode(body))
        return {
                "subject": subject,
                "from": from_email,
                "to": to_email,
                "date": date,
                "body": body
                #"metadata": headers
            }
        
    
    def decode_mime_header(self, header_val: str) -> str:
        if not header_val:
            return ""
        decoded_parts = decode_header(header_val)
        return "".join(
            str(t[0], t[1] or "utf-8") if isinstance(t[0], bytes) else str(t[0])
            for t in decoded_parts
        )

    def get_label_id(self, service, label_name):
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