from typing import Optional, Dict

import requests

from exceptions import ServiceUnavailableException


def fetch_data(url: str, params: Optional[Dict] = None):
    response = requests.get(url, params=params or {})
    return response.json()


def send_data(url: str, payload: dict):
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
