from tavily import TavilyClient
import os

from dotenv import load_dotenv


load_dotenv()


def web_search(query:str):
    """
    Searches the web for up-to-date information.

    Args:
        query: The search query.

    Returns:
        A list of relevant web search results.
    """

    client=TavilyClient(api_key=load_dotenv("TAVILY_API_KEY"))

    response= client.search(query=query,max_results=5)

    results=[]

    for result in response["results"]:

        results.append({
            "title":result["title"],
            "url":result["url"],
            "content":result["content"]
        }
        )

    return results
