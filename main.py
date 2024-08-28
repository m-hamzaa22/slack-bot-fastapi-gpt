import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import openai

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Environment variables (consider using a more secure way to manage these)
SLACK_BOT_TOKEN = 'Your Bot Tokem'
OPENAI_API_KEY = 'Your Open API key'

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

# Store processed message IDs to avoid duplicates
processed_message_ids = set()

# Define data models
class SlackEvent(BaseModel):
    type: str
    event: dict = None
    challenge: str = None

class ChatRequest(BaseModel):
    user_id: str
    message: str
    message_id: str

def is_message_processed(message):
    msg_id = message.get('client_msg_id') or message.get('ts')
    if msg_id:
        if msg_id in processed_message_ids:
            return True
        else:
            processed_message_ids.add(msg_id)
            return False
    return False

@app.post('/slack/events')
async def handle_event(request: Request):
    body = await request.json()
    slack_event = SlackEvent(**body)

    # Handle Slack URL verification
    if slack_event.type == "url_verification":
        logging.info("Handling Slack URL verification")
        return JSONResponse(content={"challenge": slack_event.challenge})

    # Handle Slack event callback
    if slack_event.type == "event_callback":
        event = slack_event.event
        if event.get("type") == "message":
            user_message = event.get("text", "")
            channel_id = event.get("channel", "")
            message_id = event.get("client_msg_id", "")
            user_id = event.get("user", "")
            bot_id = event.get("bot_id", None)

            # Log the entire event payload for debugging
            logging.info(f"Received Slack event: {event}")

            # Check if the message ID has been processed
            if is_message_processed(event):
                logging.info(f"Message with ID {message_id} already processed.")
                return JSONResponse(content={"response": "Message already processed."})

            # Check if the message ID is present
            if not message_id and not bot_id:
                logging.warning("Message ID is missing and message is from user.")
                return JSONResponse(content={"response": "Message ID is missing."})

            # Check if the message is from a bot
            if bot_id:
                logging.info("Ignoring message from bot.")
                return JSONResponse(content={"response": "Message from bot ignored."})

            # Forward the message to the chatbot
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(
                        "http://localhost:8000/chatbot",
                        json={
                            "user_id": user_id,
                            "message": user_message,
                            "message_id": message_id
                        }
                    )
                    if response.status_code == 200:
                        reply = response.json().get("response", "")
                    else:
                        logging.error(f"Error from chatbot endpoint: {response.text}")
                        reply = "Sorry, an error occurred while processing your request."

                except httpx.RequestError as e:
                    logging.error(f"HTTP Request error: {str(e)}")
                    reply = "Sorry, an error occurred while sending the request."

                # Send the reply back to Slack
                try:
                    await client.post(
                        "https://slack.com/api/chat.postMessage",
                        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
                        data={"channel": channel_id, "text": reply}
                    )
                except httpx.RequestError as e:
                    logging.error(f"HTTP Request error while posting message to Slack: {str(e)}")

            # Mark message ID as processed
            processed_message_ids.add(message_id)

    return JSONResponse(content={"status": "ok"})

@app.post('/chatbot')
async def chatbot(request: ChatRequest):
    try:
        user_id = request.user_id or 'anonymous'
        user_message = request.message
        message_id = request.message_id

        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        logging.debug(f"Received message from {user_id}: {user_message}")

        # Call OpenAI ChatGPT API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Please keep responses concise and to the point."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message['content']
            logging.debug(f"Generated reply for {user_id}: {reply}")

        except Exception as e:
            logging.error(f"Error occurred for {user_id}: {str(e)}")
            reply = f"Sorry, an error occurred: {str(e)}"

        return JSONResponse(content={"response": reply})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/')
async def root():
    return {"message": "Welcome to the Chatbot API!"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
