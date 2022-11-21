import requests

location = {
    "lat": 43.8,
    "lon": 6.1,
}

url = "http://localhost:9696/predict"

url = "https://61bmqgucoe.execute-api.eu-west-3.amazonaws.com/postLocation"
response = requests.post(url, json=location)
print(response.json())
