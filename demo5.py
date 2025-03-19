from openai import OpenAI
import json
import requests
from dotenv import load_dotenv
import os
from colorama import Back,Fore,Style

load_dotenv()

secret_key = os.getenv('GITHUB_TOKEN')
weather_api_key = os.getenv('WEATHER_API_KEY')

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key= secret_key
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Функция для получения погоды
def get_weather(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}&aqi=no"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp_c = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            #print(f"Weather in {location}: Temperature : {temp_c}°C, Condition : {condition}")
            print(Fore.RED + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.BRIGHT)
            print(Fore.YELLOW + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Fore.GREEN + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Fore.BLUE + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Fore.MAGENTA + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Fore.WHITE + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Back.WHITE + Fore.BLACK + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Back.YELLOW + Fore.RED + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            print(Back.MAGENTA + Fore.WHITE + f"Weather in {location}: Temperature: {temp_c}°C, Condition: {condition}" + Style.RESET_ALL)
            
        else:
            print(f"Error getting weather: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather like in Vilnius today?"}],
    tools=tools
)

# Check response
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for tool_call in tool_calls:
        if tool_call.function.name == "get_weather":
            try:
                args = json.loads(tool_call.function.arguments)
                location = args.get("location")
                if location:
                    get_weather(location)
                else:
                    print("Error: AI does not send location.")
            except json.JSONDecodeError as e:
                print(f"JSON error: {e}")
else:
    print("AI does not choose this function.")






