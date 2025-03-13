
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#  API from Hugging Face
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/Qwen/QwQ-32B" 

HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Init of Streamlit
st.set_page_config(page_title="Chatbot", page_icon="💬")

st.title("😺  Alex-Chatbot  ")

# Init of chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# View of chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Response function from Hugging Face
def get_response(prompt):
     # Add instruction to always reply in Lithuanian
    instruction = "Atsakyk į šį klausimą lietuvių kalba: "
    full_prompt = f"{instruction}{prompt}"
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.json()}"


# user input
if prompt := st.chat_input("Įveskite savo žinutę čia..."):
    # add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # View user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate answer
    with st.spinner("Thinking...""Mąstau..."):
        reply = get_response(prompt)

        # Response view
        with st.chat_message("assistant"):
            st.markdown(reply)

        # history
        st.session_state.messages.append({"role": "assistant", "content": reply})









