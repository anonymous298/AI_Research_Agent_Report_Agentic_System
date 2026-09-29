from agents import Agent, Runner, Trace
from dotenv import load_dotenv
import asyncio

load_dotenv(override=True)


agent = Agent(
    name="Report Agent",
    instructions="You are a Report Agent You create brief report on user prompts keyword",
    model="gpt-5-mini",
)

if __name__ == "__main__":
    response = asyncio.run(Runner.run(agent, "Create a short report on what is AI"))
    print(response.final_output)