import chainlit as cl
from main import myAgent

@cl.on_chat_start
async def chat_start():
    # Send a greeting message when chat starts
    await cl.Message(content="Hello! How can I help you?").send()

@cl.on_message
async def main(message: cl.Message):
    # Get user input from the chat message
    user_input = message.content
    
    # Get the agent's response asynchronously
    response = await myAgent(user_input)
    
    # Send the agent's response back to the chat
    await cl.Message(content=response).send()
