
import asyncio

from dotenv import load_dotenv
from app.agents import planner
from app.agents.researcher import run_research_agent
from app.agents.writer import run_writer
from app.services.search_executor import SearchExecutor
from app.workflows.conversation_workflow import ConversationWorkflow

load_dotenv(override=True)  # must run first so LANGSMITH_* reach os.environ

from agents import set_trace_processors
from langsmith.integrations.openai_agents_sdk import OpenAIAgentsTracingProcessor

set_trace_processors([OpenAIAgentsTracingProcessor()])

class ResearchWorkflow:
    def __init__(self) -> None:
        pass

    async def research_planning(self, query: str):
        """ Starts Planning and give us the structured output with intent and search_queries """

        try:
            # comment: Executing the Planning SDK using planner.py 

            planner_structured_output = await planner.plan(query)

            # checking if its intent is converation so redirect to normal llm
            if planner_structured_output.intent == "conversation":
                conversation_flow = ConversationWorkflow()

                conversation_response = await conversation_flow.run(query)

                return (
                    planner_structured_output.intent,
                    conversation_response,
                )

            elif planner_structured_output.intent == "research":
                # Performing Asyncrounous Searches simultaneously
                search_executor = SearchExecutor()

                if planner_structured_output.search_queries:
                    searches_result = await search_executor.async_searches(planner_structured_output.search_queries)

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
            
            #running the research_planning block
            intent, output_result = await self.research_planning(query)

            if intent == "conversation":
                return {
                    "intent" : intent,
                    "message" : output_result,
                    "sources" : [],
                }

            #performing Research using Reserach Agent
            researched_output = await run_research_agent(query, output_result)

            
            # Feeding researched output to writer agent
            writer_output = await run_writer(query, researched_output)

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

        response = await workflow.run_research_workflow(research_test_case)

        print(f"Intent: {response['intent']}")
        print(f"Message: {response['message']}")
        print(f"Sources: {response['sources']}")

    print("workflow running...")
    asyncio.run(main())