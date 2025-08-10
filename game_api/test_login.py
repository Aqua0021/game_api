import requests

url = "http://127.0.0.1:5000/login"
data = {"username": "aqua", "password": "1234"}  # use a real registered account

response = requests.post(url, json=data)
print(response.json())
