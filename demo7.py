
from rich import print
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
import json
from colorama import Back, Fore, Style

load_dotenv()

secret_key = os.getenv('GITHUB_TOKEN')

if secret_key is None:
    print("Please set GITHUB_TOKEN in .env file")

def read_from_file(filename: str = "vilnius.txt"):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found. Please make sure the file exists."

def write_to_file(content: str, filename: str = "summary.txt"):
    if content is None:
        raise ValueError("Cannot write 'None' to a file.")
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return os.path.abspath(filename)

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=secret_key
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_from_file",
            "description": "Read content from a given file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                },
                "required": ["filename"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_to_file",
            "description": "Write content to a file and return the absolute path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# === Step 1: Read content from file ===
completion_1 = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Please read the content from the file vilnius.txt"}],
    tools=tools
)

tool_call_1 = completion_1.choices[0].message.tool_calls[0]
args_1 = json.loads(tool_call_1.function.arguments)

content_from_file = read_from_file(args_1["filename"])
print(f"[bold green]Content from file:[/bold green]\n{content_from_file}")

# === Step 2: Generate a summary ===
messages = [
    {"role": "user", "content": "Please summarize the following content:"},
    {"role": "assistant", "content": content_from_file}
]

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

summary = completion_2.choices[0].message.content

# Проверяем, сгенерировала ли модель текст
if summary is None:
    print("[bold red]Error:[/bold red] No summary was generated.")
else:
    print(f"[bold blue]AI Generated Summary:[/bold blue]\n{summary}")

    # === Step 3: Write the summary to a new file ===
    completion_3 = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Please write this summary into a new file."},
            {"role": "assistant", "content": summary}
        ],
        tools=tools
    )

    # Проверяем вызов инструмента
    if completion_3.choices[0].message.tool_calls:
        tool_call_3 = completion_3.choices[0].message.tool_calls[0]
        args_3 = json.loads(tool_call_3.function.arguments)

        if tool_call_3.function.name == "write_to_file":
            file_path = write_to_file(args_3["content"])
            print(f"[bold green]Summary written to:[/bold green] {file_path}")
