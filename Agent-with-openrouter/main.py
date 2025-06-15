import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled

# Load .env file
load_dotenv()

# Disable internal tracing
set_tracing_disabled(True)

# Set up the OpenRouter API client
provider = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"  # ✅ Make sure this URL is correct
)

# Use a known working model (you can try gpt-3.5 if gemini fails)
model = OpenAIChatCompletionsModel(
    model="openai/gpt-3.5-turbo",  # ✅ Replace with your supported model if needed
    openai_client=provider,
)

# Define the agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model
)
long_question = """
I'm trying to understand the concept of decorators in Python, especially how @property, @setter, and @deleter work together. 
Could you explain this in simple terms with a class example that uses all three decorators?
"""

# Run the agent
response = Runner.run_sync(
    starting_agent=agent,
    input=long_question
)

# Print the final output
print(response.final_output)
 