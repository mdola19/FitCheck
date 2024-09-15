#pip install groq
from groq import Groq
import json, requests, os

#test data
tops = [
    "blue sweater",
    "black hoodie",
    "white t-shirt",
    "red flannel shirt",
    "gray jacket"
]

# List of bottoms
bottoms = [
    "blue jeans",
    "black chinos",
    "gray sweatpants",
    "brown corduroys",
    "khaki shorts"
]

# List of footwear
footwear = [
    "white sneakers",
    "black boots",
    "brown loafers",
    "gray running shoes",
    "blue sandals"
]

#wrapper function to update json files 
def add_location_to_json(file_path, location, location_value):
    # Check if the file exists and has content
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Open and read existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        # If file doesn't exist or is empty, create an empty dictionary
        data = {}

    # Add or update the new location in the dictionary
    data[location] = location_value

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def formatWeatherData(data):
    package = 0
    AvgTemp = []
    isRain = []
    isCloudy = []
    dailytemp = 0;
    dailyrain = False
    dailycloudy = False
    for i in range(4):
        for j in range(8):
            dailytemp += data["list"][package]["main"]['temp']    
            if not dailyrain and data["list"][package]["weather"][0]['main'] == "Rain":
                dailyrain = True
                dailycloudy = True

            elif not dailycloudy and data["list"][package]["weather"][0]['main'] == "Cloud":
                dailycloudy = True
            
            package +=1   

        AvgTemp.append(dailytemp/8)
        isRain.append(dailyrain)
        isCloudy.append(dailycloudy)

        dailytemp = 0
        dailycloudy = False
        dailyrain = False

    return AvgTemp, isRain, isCloudy


#open config file to import api keys
with open('config.json', 'r') as file:
    config = json.load(file)

# Accessing the API keys
openweather_api_key = config['openweather_api_key']
groq_api_key = config['groq_api_key']

# Open and read the JSON file
with open('locations.json', 'r') as file:
    locationdata = json.load(file)

#getting location
location = "yellowknife"
locationvalue = None

#checks if location is already stored, if not gets data
if location in locationdata:
    locationvalue = locationdata.get(location)
    WeatherDataUrl = "https://api.openweathermap.org/data/2.5/forecast?" + f"lat={locationvalue[0][1]}&lon={locationvalue[0][1]}" + "&cnt=32&units=metric&appid=93e6779383952f5bf1144fbc6e0f18da"
    
else:
    location_url = "http://api.openweathermap.org/geo/1.0/direct?q=" + location+ ",CA" + "&limit=1&appid=" + openweather_api_key
    print(location_url)
    locationrequest = requests.get(location_url).json()
    locationvalue = [locationrequest[0]["lat"],locationrequest[0]['lon']]
    WeatherDataUrl = "https://api.openweathermap.org/data/2.5/forecast?" + f"lat={locationvalue[0]}&lon={locationvalue[1]}" + "&cnt=32&units=metric&appid=93e6779383952f5bf1144fbc6e0f18da"
    WeatherData = requests.get(WeatherDataUrl).json()
    add_location_to_json("locations.json",location, [locationvalue,formatWeatherData(WeatherData)])

with open('locations.json', 'r') as file:
    locationdata = json.load(file)


#Intialise LLM
client = Groq(api_key=groq_api_key)
completion = client.chat.completions.create(
    model="gemma2-9b-it",
    messages=[
        {
            "role": "user",
            "content": f"Im giving you data like so [[avg temperature of day 1, avg temperature of day 2, avg temperature of day 3, avg temperature of day 4], [if it rains on day 1,if it rains on day 2, if it rains on day 3, if it rains on day 4], [if its cloudy on day 1, if its cloudy on day 2, if its cloudy on day 3, if its cloudy on day 4]]]. Here is the data{locationdata.get(location)[1]} Give me four outfits using these tops {tops} these bottoms{bottoms} and these footwear{footwear}, one for each day consisting of 3 articles: top, bottom and shoes and make sure the combinations are stylish. Return the result as a list of just the clothes and no identifiers. dont reuse clothes and only give the list, no reasoning, no commas, ONLY WHITESPACE AS SEPERATOR, extra bits, or python wrapper for formating"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

result = ""
days = [[],[],[],[]]

for chunk in completion:
    result += (chunk.choices[0].delta.content or "")


span = 2
result = result.split()
result = [" ".join(result[i:i+span]) for i in range(0, len(result), span)]

for i in range(4):
    for j in range(3):
        days[i].append(result[j+(i*3)])

print(days)
