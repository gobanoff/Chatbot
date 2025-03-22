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





    
