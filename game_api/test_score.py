import requests

url = "http://127.0.0.1:5000/get_scores?game=easy_car"
response = requests.get(url)
print(response.json())
