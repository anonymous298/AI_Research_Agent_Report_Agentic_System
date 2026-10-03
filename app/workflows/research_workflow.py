
import asyncio
import selectors

from dotenv import load_dotenv
from app.agents import planner
from app.agents.researcher import run_research_agent
from app.agents.writer import run_writer
from app.core.database import AsyncSessionLocal, init_db
from app.memory.schemas import ResearchMemory
from app.services.search_executor import SearchExecutor
from app.workflows.conversation_workflow import ConversationWorkflow
from app.memory.service import MemoryService

load_dotenv(override=True)  # must run first so LANGSMITH_* reach os.environ

from agents import set_trace_processors
from langsmith.integrations.openai_agents_sdk import OpenAIAgentsTracingProcessor

set_trace_processors([OpenAIAgentsTracingProcessor()])

class ResearchWorkflow:
    def __init__(self) -> None:
        self.conversation_flow = ConversationWorkflow()
        self.search_executor = SearchExecutor()
        self.memory_service =  MemoryService()

    async def retrieve_similar_memories_db(self, query: str) -> str:
        """  Retrieve similar memories with db connection """

        try:

            LIMIT=5

            async with AsyncSessionLocal() as session:
                similar_memories = await self.memory_service.retrieve_similar_searches(session, query, LIMIT)

                memory_context = "\n".join(
                    f"- Topic: {m.topic}\n"
                    f"  Content: {m.content}\n"
                    f"  Source: {m.source_url}"
                    for m in similar_memories
                )

                print(memory_context)

                return memory_context

        except Exception as e:
            print(f"research workflow retrieving similar memories failed: {e}")
            return f"research workflow retrieving similar memories failed: {e}"


    async def save_memory(self, user_query: str, content: str, source_url: str):
        """ Saving all memories """

        try: 

            memory = ResearchMemory(
                topic=user_query,
                content=content,
                source_url=source_url,
            )

            async with AsyncSessionLocal() as session:
                saved_memory = await self.memory_service.save_memory(session, memory)

                if saved_memory:
                    return "memory added"

        except Exception as e:
            print(f"research workflow saving memory failed: {e}")
            return f"research workflow saving memory failed: {e}"

    async def research_planning(self, query: str, similar_relevant_memories: str):
        """ Starts Planning and give us the structured output with intent and search_queries """

        try:


            # comment: Executing the Planning SDK using planner.py 
            planner_structured_output = await planner.plan(query)

            # checking if its intent is converation so redirect to normal llm
            if planner_structured_output.intent == "conversation":
                # conversation_flow = ConversationWorkflow()

                conversation_response = await self.conversation_flow.run(query, similar_relevant_memories)

                return (
                    planner_structured_output.intent,
                    conversation_response,
                )

            elif planner_structured_output.intent == "research":
                # Performing Asyncrounous Searches simultaneously
                # search_executor = SearchExecutor()

                if planner_structured_output.search_queries:
                    searches_result = await self.search_executor.async_searches(planner_structured_output.search_queries)

                    return (
                        planner_structured_output.intent,
                        searches_result,
                    )

        except Exception as e:
            print(f"research planning step failed: {e}")
            return f"research planning step failed: {e}"
        # end try

    async def run_research_workflow(self, query: str):
        ''' Starts the main workflow chain '''

        try:
            # connecting database
            await init_db()


            # Retrieving Similar Memories based on query
            similar_relevant_memories = await self.retrieve_similar_memories_db(query)
            
            #running the research_planning block
            intent, output_result = await self.research_planning(query, similar_relevant_memories)

            if intent == "conversation":
                adding_memory = await self.save_memory(query, output_result, "www.example.com")

                return {
                    "intent" : intent,
                    "message" : output_result,
                    "sources" : [],
                }

            #performing Research using Reserach Agent
            researched_output = await run_research_agent(query, output_result, similar_relevant_memories)

            
            # Feeding researched output to writer agent
            writer_output = await run_writer(query, researched_output)

            #saving memory
            saving_memory = await self.save_memory(query, writer_output.answer, writer_output.sources[0].url)

            return {
                "intent" : intent,
                "message" : writer_output.answer,
                "sources" : writer_output.sources,
            }
 

        except Exception as e:
            print(f"research main workflow failed: {e}")
            return {
                "intent": "error",
                "message": f"Research workflow failed: {e}",
                "sources": [],
            }



# testing
if __name__ == "__main__":
    async def main():
        workflow = ResearchWorkflow()

        conversation_test_case = "Whats the difference between async and sync programming in Python?"
        research_test_case = "Research how Redis is used in production AI agent systems, including caching, rate limiting, and background task coordination."
        research_test_case2 = "What are the latest trends in AI agents for business automation in 2026, and which tasks are companies actually automating with them?"

        response = await workflow.run_research_workflow(research_test_case2)

        print(f"Intent: {response['intent']}")
        print(f"Message: {response['message']}")
        print(f"Sources: {response['sources']}")

    print("workflow running...")
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))