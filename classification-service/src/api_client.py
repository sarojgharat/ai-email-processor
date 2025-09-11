import requests

def classify_text(process: str, text: str, host: str = "http://localhost", port: int = 8001):
    url = f"{host}:{port}/classify"
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

# Example usage
if __name__ == "__main__":
    result = classify_text(
        process="booking",
        text="New Booking Request",
        host="http://localhost",
        port=8001
    )
    print("Classification Result:", result)