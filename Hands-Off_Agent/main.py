from dotenv import load_dotenv
from agents import  Agent,Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os

load_dotenv() 
set_tracing_disabled(True)

provider = AsyncOpenAI(
    api_key = os.getenv('GEMINI_API_KEY'),
    base_url ="https://generativelanguage.googleapis.com/v1beta/openai/" 
)
model = OpenAIChatCompletionsModel(
    model ="gemini-2.0-flash-exp",
    openai_client=provider,
)
web_dev  = Agent( 
 name="Website Developer", 
 instructions="Build website using modern frameworks and tools.", 
 model=model,
 handoff_description="handoff to Website Developer if the task is related to website.", 
)
mobile_dev = Agent(
    name="Mobile Developer",
    instructions="Build mobile apps using modern frameworks and tools.",
    model=model,
    handoff_description="handoff to mobile developer if the task is related to mobile app development.",
)
marketing = Agent( 
 name="Marketing Agent", 
 instructions="Create and execute marketing strategies for product launches.", 
 model=model, 
 handoff_description="handoff to marketing agent if the task is related to marketing.", 
) 
async def my_agent(user_input):
    manager = Agent( 
 name="Manager", 
 instructions="You will chat with the user and delegate tasks to specialized agents based on their requests.", 
 model=model,
 handoffs=[web_dev, mobile_dev, marketing] 
    )

    response = await Runner.run(
      manager,
      input = user_input,
  )
    return response.final_output 