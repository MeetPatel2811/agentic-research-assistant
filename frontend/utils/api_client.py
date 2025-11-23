import requests

API_URL = "http://localhost:8000/query"

def ask_backend(query: str):
    response = requests.post(API_URL, json={"query": query})
    if response.status_code == 200:
        return response.json().get("response", "")
    return "Error: API call failed."
