import requests
from config import API_BASE_URL

def login(username, password):
    url = f"{API_BASE_URL}/login/"
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Server not reachable"}

def signup(username, email, password):
    url = f"{API_BASE_URL}/signup/"
    data = {"username": username, "email": email, "password": password}
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Server not reachable"}
