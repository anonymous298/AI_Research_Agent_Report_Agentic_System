
import asyncio
from openai import AsyncOpenAI

from app.config import settings
from dotenv import load_dotenv

load_dotenv(override=True)

class ConversationWorkflow:
    def __init__(self) -> None:
        pass


    async def run(self, query: str) -> str:
        ''' Run the normal LLM Call '''

        try:

            conversation_prompt = open("app/prompts/conversation.md").read()

            client = AsyncOpenAI()

            response = await client.responses.create(
                model=settings.model,
                instructions=conversation_prompt,
                input=query,
            )
            
            if response.output_text:
                return response.output_text

            else:
                print("No Model Output")

        except Exception as e:
            print(f"conversation executing step failed: {e}")




# Testing 
if __name__ == "__main__":

    async def main():
        conversation = ConversationWorkflow()

        response = await conversation.run("Hi, how are you?")

        print(response)

    print("Conversation testing...")
    asyncio.run(main())
