import os
from google import genai
from google.genai import types
from rich import print
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the client
client = genai.Client(api_key=gemini_api_key)

# Open and read the image file
with open("54098431857_755c192932_o.jpg", "rb") as f:
    image = f.read()

# Generate content using the Gemini model
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(data=image, mime_type="image/jpg"),
        "Apibūdinkite šios nuotraukos išvaizdą lietuvių kalba.",
    ],
)

# Print the response in Lithuanian
print(response.text)
