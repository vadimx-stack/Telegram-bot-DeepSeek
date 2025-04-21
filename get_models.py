import requests
from pprint import pprint


url = "https://api.intelligence.io.solutions/api/v1/models"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer ",  
}

response = requests.get(url, headers=headers)
data = response.json()
pprint(data)

for i in range(len(data['data'])):
    name = data['data'][i]['id']
    print(name) 