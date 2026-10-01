# app/tools/search.py
from agents import function_tool, RunContextWrapper
from app.context import AppContext
from app.config import settings

@function_tool
async def web_search(ctx: RunContextWrapper[AppContext], query: str, num_results: int = 3) -> str:
    """Search Google for current information and return the top results.

    Args:
        query: Short, specific search phrase.
        num_results: How many results to return (1-3).
    """

    try: 

        res = await ctx.context.http.post(
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
        print(f"Research Tool Failed: {e}")
        return f"research tool failed: {str(e)}"
