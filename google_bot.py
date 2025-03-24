
import streamlit as st
import google.generativeai as genai
import os


# Path to json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Home\\Desktop\\рython\\rag_ai\\chatbot-454519-5952946456ae.json"

#  API (use Service Account, no api_key)
genai.configure()

# Configure the API key
#genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Streamlit app setup
st.set_page_config(page_title="Google-Chatbot")
st.title("🤖 Google-Chatbot")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask me something...")
if prompt:
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    response = model.generate_content([prompt]).text
    
    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})











   
    