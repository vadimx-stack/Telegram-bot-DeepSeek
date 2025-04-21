import requests
from pprint import pprint

url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ",
}

data = {
    "model": "deepseek-ai/DeepSeek-R1",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": "how are you doing"
        }
    ],
}

response = requests.post(url, headers=headers, json=data)
data = response.json()
pprint(data) 

text = data['choices'][0]['message']['content']
print(text.split('</think>\n\n')[1]) 