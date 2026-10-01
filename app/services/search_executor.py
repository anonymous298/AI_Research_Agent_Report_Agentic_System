# app/tools/search.py
import asyncio
from agents import RunContextWrapper
from app.config import settings
import httpx


class SearchExecutor:

    async def web_search(self, client: httpx.AsyncClient, query: str, num_results: int = 1) -> str:
        """ Query web for each terms async nature can use this single function as many times in async nature """

        try: 

            res = await client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": settings.serper_api_key},
                json={"q": query, "num": num_results},
            )
            res.raise_for_status()
            items = res.json().get("organic", [])

            for i in items:
                print(i["title"], i["link"])

            return "\n\n".join(
                f"{i['title']}\n{i['link']}\n{i.get('snippet', '')}" for i in items
            )
        
        except Exception as e:
            print(f"individual async web search service failed: {e}")
            return f"individual async web search service failed: {str(e)}"



    async def async_searches(self, search_queries: list[str]):
        """ Performs Async Web Searches Simultaneously """

        try:

            async with httpx.AsyncClient(timeout=20) as http:
                searches_result = await asyncio.gather(
                    *(self.web_search(http, query) for query in search_queries)
                )

                return searches_result
        
        except Exception as e:
            print(f"async web searches failed: {e}")
            return f"async web searches failed: {e}"




# Testing 
if __name__ == "__main__":
    async def main():
        search_executor = SearchExecutor()

        result = await search_executor.async_searches(["OpenAI Agents SDK latest features", "OpenAI Agents SDK production best practices", "OpenAI Agents SDK architecture", "OpenAI Agents SDK documentation"])

        print(result)

    print("Testing Search Executor...")
    asyncio.run(main())