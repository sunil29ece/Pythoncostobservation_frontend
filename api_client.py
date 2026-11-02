import os
import requests

API_URL = os.getenv('API_URL', 'http://localhost:8000').rstrip('/')

def get_cost_analysis():
    response = requests.get(f'{API_URL}/cost-analysis', timeout=15)
    response.raise_for_status()
    return response.json()
