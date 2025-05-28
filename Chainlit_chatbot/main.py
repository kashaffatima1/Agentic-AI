from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import os
import asyncio

# Load environment variables
load_dotenv()

# Disable tracing
set_tracing_disabled(True)

# Create OpenAI/Gemini provider
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Set up the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider,
)

# Define async agent function
async def myAgent(user_input):
    Agent1 = Agent(
        name="Assistant",
        instructions="A helpful assistant that can answer questions and provide information.",
        model=model
    )

    response = await Runner.run(
        starting_agent=Agent1,
        input=user_input,
    )

    return response.final_output
