
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from colorama import Back,Fore,Style


load_dotenv()

# Access the secret
secret_key = os.getenv("GITHUB_TOKEN")


client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key= secret_key
)
#client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather like in Vilnius today?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)

tool_calls = completion.choices[0].message.tool_calls

tool_calls_data = [
        {
            "function_name": tool_call.function.name,
            "arguments": tool_call.function.arguments
        }
        for tool_call in tool_calls
    ]

tool_calls_str = json.dumps(tool_calls_data, indent=2)

print(Back.MAGENTA + Fore.WHITE + tool_calls_str + Style.RESET_ALL)
