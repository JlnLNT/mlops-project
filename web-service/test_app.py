import requests

location = {
    "lat": 43.8,
    "lon": 7.1,
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=location)
print(response.json())