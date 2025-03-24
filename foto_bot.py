import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io
from google.cloud import vision


# Path to json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Home\\Desktop\\рython\\rag_ai\\chatbot-454519-5952946456ae.json"

# API (use Service Account, no api_key)
genai.configure()

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Streamlit app setup
st.set_page_config(page_title="Google-Photo-Chatbot")
st.title("😺 Google-Photo-Chatbot 😺")

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

# Image upload functionality
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    # Process the image (Here you could use a model or API like Google Vision)
    image = Image.open(uploaded_file)

    # Convert image to bytes for processing if needed
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    description = model.generate_content([f"Describe this image: {uploaded_file.name}"]).text
    
    
    st.write("Description of the image:")
    st.write(description)




    




