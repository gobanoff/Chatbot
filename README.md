# Alex-Chatbot

## Description

**Alex-Chatbot** is a conversational AI built using Streamlit and the Hugging Face API. It provides an interactive chatbot interface where users can ask questions, and the chatbot will respond in Lithuanian. The application is powered by a Hugging Face model and is easy to set up with minimal dependencies.

## Features

- **Chat Interface**: A simple and interactive chat interface to talk to the AI.
- **Lithuanian Language**: The chatbot always responds in Lithuanian.
- **Hugging Face Integration**: Uses Hugging Face's API to generate AI responses.
- **State Management**: Keeps track of the chat history so that users can have a continuous conversation.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- Streamlit
- Requests
- python-dotenv

### Installation

1. Clone this repository:
    ```powershell
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```powershell
    cd <project_directory>
    ```

3. Create and activate a virtual environment: 

    ```powershell
    uv venv 
    .\venv\Scripts\Activate
    ```

4. Install the required dependencies:
    ```powershell
    pip install -r requirements.txt
    use 'uv add' + 'your dependencies'command to install
    ```

5. Create a .env file in the root directory of the project and add your Hugging Face API key:
    ```powershell
    HUGGINGFACE_API_KEY=<your_hugging_face_api_key>
    ```

## Running the Application

To start the chatbot app, run the following command:

```powershell
streamlit run demo3.py
