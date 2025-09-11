import requests

def extract_data(process: str, category: str, text: str, host: str = "http://localhost", port: int = 8003):
    url = f"{host}:{port}/extract"
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

# Example usage
if __name__ == "__main__":
    result = extract_data(
        process="booking",
        category="booking request",
        text="Your flight to Tokyo is confirmed for October 15."
    )
    print("Extracted Data:", result)