import requests

def fetch_data(url: str):
    print(f"URL ES {url}")
    response = requests.get(url)
    return response.json()

def send_data(url: str, payload: dict):
    print(f"URL ES {url}")
    response = requests.post(url , json=payload)
    response.raise_for_status()
    return response.json()