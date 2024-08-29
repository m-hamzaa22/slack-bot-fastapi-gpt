# FastAPI Slack Chatbot Integration

This project integrates Slack with OpenAI's GPT-3.5-turbo using FastAPI. The application listens for events from Slack, processes incoming messages, and responds using the OpenAI ChatGPT model.

## Features

- **Slack Event Handling**: Receives and processes events from Slack.
- **Message Processing**: Avoids duplicate processing of messages.
- **ChatGPT Integration**: Utilizes OpenAI's ChatGPT to generate responses.
- **Logging**: Provides detailed logs for debugging and monitoring.

## Prerequisites

- Python 3.8 or higher

## Installation

1. **Clone the repository:**
     ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository

Create and activate a virtual environment (optional but recommended)

bash

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required packages:

Install dependencies from requirements.txt:

      pip install -r requirements.txt

Set environment variables for Slack and OpenAI:

For Unix-based systems (Linux, macOS):
        
      export SLACK_BOT_TOKEN='Your Slack Bot Token'
      export OPENAI_API_KEY='Your OpenAI API Key'

**For Windows:**

cmd

    set SLACK_BOT_TOKEN=Your Slack Bot Token
    set OPENAI_API_KEY=Your OpenAI API Key

Configuration

    SLACK_BOT_TOKEN: Your Slack Bot Token.
    OPENAI_API_KEY: Your OpenAI API Key.

Ensure that these environment variables are set before running the application.
Usage

    Run the FastAPI application:

    bash

    uvicorn main:app --host 0.0.0.0 --port 8000

    The application will be accessible at http://localhost:8000.

Endpoints

    POST /slack/events: Receives events from Slack and processes messages.
    POST /chatbot: Forwards user messages to the ChatGPT model and returns responses.
    GET /: Returns a welcome message.

**Logging**

Logging is configured to provide detailed information about the application's operation and any errors encountered. Logs are output to the console.

**Error Handling**

The application includes basic error handling for request errors and exceptions. Ensure to check the logs for detailed error messages.

**Security**

For a production setup, consider using a more secure method for managing environment variables and sensitive information.

*
**License**
This project is licensed under the MIT License. See the LICENSE file for details.

**Contributing**

Feel free to submit issues, suggestions, or pull requests.

**Contact**

For any questions, please contact [m.hamzaa1218@gmail.com].
