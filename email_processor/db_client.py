import requests

BASE_URL = "http://localhost:8080/email"

def create_email_request(payload):    
    response = requests.post(BASE_URL + "/", json=payload)
    #print("Create Response:", response.json())

def get_email_request(request_id):
    response = requests.get(f"{BASE_URL}/{request_id}")
    #print("Get Response:", response.json())

def update_email_request(request_id, update_payload):
    response = requests.put(f"{BASE_URL}/{request_id}", json=update_payload)
    #print("Update Response:", response.json())

def delete_email_request(request_id):
    response = requests.delete(f"{BASE_URL}/{request_id}")
    #print("Delete Response:", response.json())

if __name__ == "__main__":
    payload = {
        "request_id": "REQ001",
        "business_process": "Invoice Processing",
        "original_email": {
            "subject": "Invoice for March",
            "body": "Please find attached the invoice for March.",
            "sender": "accounts@example.com"
        }
    }

    update_payload = {
        "classification_type": "Finance"
    }
    

    create_email_request(payload)
    get_email_request("REQ001")
    update_email_request("REQ001", update_payload)
    delete_email_request("REQ001")