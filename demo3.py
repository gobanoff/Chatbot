from openai import OpenAI

import os
from dotenv import load_dotenv
import streamlit as st
import PyPDF2
from docx import Document

st.title("ChatGPT-like clone")
# Load environment variables from .env file
load_dotenv()

# Access the secret
secret_key = os.getenv("GITHUB_TOKEN")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key= secret_key
)

st.markdown("""
    <style>
        /* Body Styling */
        .main { 
            background-color: #ff0000 !important;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Arial', sans-serif;
        }

        /* Styling the Title */
        h1 {
            color: #4CAF50;
            text-align: center;
            font-size: 3em;
        }

        /* Chat History Container */
        .chat-history-container {
            background-color: #ff0000 !important;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ccc;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: scroll;
        }

        /* Styling the message */
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 8px;
        }

        .message.user {
            background-color: #f0f8ff;
            border-left: 5px solid #4CAF50;
        }

        .message.assistant {
            background-color: #e0e0e0;
            border-left: 5px solid #2196F3;
        }

        /* File uploader style */
        .file-uploader {
            padding: 10px;
            background-color:#ff0000 !important;
            border-radius: 8px;
            border: 1px solid #ccc;
        }

        /* Input Box Styling */
        .stTextInput, .stTextArea {
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 12px;
            width: 100%;
            box-sizing: border-box;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
        }

        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>"""
, unsafe_allow_html=True)



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history in a bordered container
with st.container():
    st.subheader("Chat History")
    if not st.session_state.messages:
        st.info("No messages yet. Start the conversation!")
    else:
        for message in st.session_state.messages:
            with st.expander(f"{message['role'].capitalize()} says:"):
                st.markdown(message["content"])

 
          



# Handle file upload
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

if uploaded_file:
    # Extract text depending on file type (for example, PDF or DOCX)
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'txt':
        file_text = uploaded_file.read().decode("utf-8")
    elif file_extension == 'pdf':
        
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        file_text = ""
        for page in pdf_reader.pages:
            file_text += page.extract_text()
    elif file_extension == 'docx':
       
        doc = Document(uploaded_file)
        file_text = "\n".join([para.text for para in doc.paragraphs])
    else:
        file_text = "Unsupported file type"

 # Show extracted text
    st.text_area("Extracted text from file", file_text, height=200)



system_message = {
    "role": "system",
    "content": "Atsakyk tik lietuviškai, net jei klausimas yra kita kalba. Neatsakyk jokia kita kalba, išskyrus lietuviu kalbą."
}


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                system_message,  
                *st.session_state.messages
            ],
          #  messages=[
              #  {"role": m["role"], "content": m["content"]}
               # for m in st.session_state.messages
          #  ],
            stream=True,
        )
        response = st.write_stream(stream)
       
    st.session_state.messages.append({"role": "assistant", "content": response})





    
