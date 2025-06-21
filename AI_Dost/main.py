import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load env variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not found")

# Run when chat starts
@cl.on_chat_start
async def chat_start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    model = OpenAIChatCompletionsModel(
        openai_client=external_client,
        model="gemini-2.0-flash",
    )
    
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
# Empty history
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
# Agent
    agent: Agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model
    )
    
    cl.user_session.set("agent", agent)
    
    await cl.Message(content="Welcome to AI_Dost! How can I help you today?").send()

# Run on every message
@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()
    
    try:
        agent: Agent = cast(Agent, cl.user_session.get("agent"))
        config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
        history = cl.user_session.get("chat_history") or []
        
        history.append({"role": "user", "content": message.content})
        
        result = Runner.run_sync(
            starting_agent=agent,
            input=history,
            run_config=config
        )
        
        response_content = result.final_output
        
        msg.content = response_content
        await msg.update()
        
        cl.user_session.set("chat_history", result.to_input_list())
        
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
