#pip install groq
from groq import Groq
import json

#open config file to import api keys
with open('config.json', 'r') as file:
    config = json.load(file)

# Accessing the API keys
openweather_api_key = config['openweather_api_key']
groq_api_key = config['groq_api_key']


#Intialise LLM
client = Groq(api_key=groq_api_key)
completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "user",
            "content": "Whats the weather in waterloo"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
