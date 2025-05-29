from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import os

# Load environment variables
load_dotenv()

# Disable tracing
set_tracing_disabled(True)

# Configure Gemini model via AsyncOpenAI
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Set up the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider,
)

# Define the agent
Agent1 = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that solves basic problems.",
    model=model
)

# Run agent with input
response = Runner.run_sync(
    starting_agent=Agent1,
    input="Could you share 3 programming jokes with me??",
)

# Output the result
print(response.final_output)
