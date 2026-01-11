import requests

URL = "https://your-app.vercel.app/api/state"
API_KEY = "your-secret"

data = {
    "temperature": 23.5,
    "status": "running"
}

requests.post(
    URL,
    json=data,
    headers={"Authorization": f"Bearer {API_KEY}"}
)
