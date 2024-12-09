import os
import urllib.parse
import requests
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from vectara_agentic.agent import Agent
from vectara_agentic.tools import ToolsFactory
import streamlit as st
import json, ast
from utility.temp_history import SessionHistoryManager


# Load environment variables
load_dotenv(override=True)

history_manager=SessionHistoryManager()

# google_search_results = []
# Define Pydantic schema for tool arguments
class GoogleSearchArgs(BaseModel):
    query: str = Field(..., description="The search query for Google.")

# Define output schema for individual search results
class GoogleSearchResult(BaseModel):
    title: str = Field(..., description="Title of the search result.")
    link: str = Field(..., description="URL of the search result.")
    snippet: str = Field(..., description="Snippet of the search result.")
    source: str = Field(..., description="Source of the search result.")

# Google search logic
def google_search(args: GoogleSearchArgs) -> List[dict]:
    """
    Perform a Google search using the provided query.

    Args:
        args (GoogleSearchArgs): Arguments containing the search query.

    Returns:
        List[dict]: A list of dictionaries with search result details.
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv("GOOGLE_API_KEY"),  # API key from environment variables
        "cx": os.getenv("GOOGLE_ENGINE_ID"),  # Engine ID from environment variables
        "q": urllib.parse.quote_plus(args.query),
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error during Google Search API call: {e}")
        return []
    results=[]
    if len(history_manager.get_history("xyz"))==0:
        for item in response_data.get("items", []):
            history_manager.add_entry("xyz",{
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
                "source": item.get("displayLink"),
            })
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet")})
    else:
         history_manager.clear_history("xyz")
         for item in response_data.get("items", []):
            history_manager.add_entry("xyz",{
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
                "source": item.get("displayLink"),
            })
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet")})

    return results

# Initialize ToolsFactory
tools_factory = ToolsFactory()

# Create a Google Search tool using ToolsFactory
google_search_tool = tools_factory.create_tool(
    function=lambda query: google_search(GoogleSearchArgs(query=query)), tool_type='query'
)

# Define custom instructions for the news summarization assistant
news_assistant_instructions = """
- You are a helpful news summarization assistant with expertise in generating detailed summary of at least 500 words.
- Always use the `google_search_tool` to fetch news data.
- Summarize the results using 'title' and 'snippet' keys from `google_search_tool` in a professional and detailed manner.
"""

# Create an agent with the Google Search tool and custom instructions
agent = Agent(
    tools=[google_search_tool] + tools_factory.standard_tools() + tools_factory.guardrail_tools(),
    topic="news summarization",
    custom_instructions=news_assistant_instructions,
)


async def get_news_summary(topic: str) -> dict:
    """
    Interact with the agent to get a news summary for the given topic.

    Args:
        topic (str): The topic to search for.

    Returns:
        dict: A JSON object containing the news summary and references.
    """
    return agent.chat(f"Trending news about {topic}")

# Main execution block
if __name__ == "__main__":
    topic = "AI advancements"  # Replace with your topic of interest
    summary = get_news_summary(topic)
    print(summary)

# # Define Pydantic schema for tool arguments
# class GoogleSearchArgs(BaseModel):
#     query: str = Field(..., description="The search query for Google.")

# # Define output schema for individual search results
# class GoogleSearchResult(BaseModel):
#     title: str = Field(..., description="Title of the search result.")
#     link: str = Field(..., description="URL of the search result.")
#     snippet: str = Field(..., description="Snippet of the search result.")
#     source: str = Field(..., description="Source of the search result.")

# # Define output schema for search results collection
# class GoogleSearchOutput(BaseModel):
#     results: List[GoogleSearchResult] = Field(..., description="List of search results.")

# # Function to perform Google search
# def google_search(args: GoogleSearchArgs) -> List[dict]:
#     """
#     Perform a Google search using the provided query.

#     Args:
#         args (GoogleSearchArgs): Arguments containing the search query.

#     Returns:
#         List[dict]: A list of dictionaries with search result details.
#     """
#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": os.getenv("GOOGLE_API_KEY"),  # API key from environment variables
#         "cx": os.getenv("GOOGLE_ENGINE_ID"),  # Engine ID from environment variables
#         "q": urllib.parse.quote_plus(args.query),
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
#         response_data = response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error during Google Search API call: {e}")
#         return []

#     # Parse results from API response
#     results = []
#     for item in response_data.get("items", []):
#         results.append({
#             "title": item.get("title"),
#             "link": item.get("link"),
#             "snippet": item.get("snippet"),
#             "source": item.get("displayLink"),
#         })

#     return results

# # Initialize ToolsFactory
# tools_factory = ToolsFactory()

# # Create a Google Search tool using ToolsFactory
# google_search_tool = tools_factory.create_tool(
#     function=lambda query: google_search(GoogleSearchArgs(query=query))
# )

# # Define custom instructions for the news summarization assistant
# news_assistant_instructions = """
# - You are a helpful news summarization assistant with expertise in current events reporting.
# - Never discuss politics and always respond politely.
# - Always use the google_search_tool to fetch news data.
# - Summarize the results in a professional and concise manner.
# - Provide a list of sources and links from the google_search_tool as citations.
# - OUTPUT MUST BE IN JSON FORMAT:
#   {{
#     "SUMMARY": "summary generated",
#     "REFERENCES": "valid links (URLs) of news from google_search_tool"
#   }}
# """

# # Create an agent with the Google Search tool and custom instructions
# agent = Agent(
#     tools=[google_search_tool] + tools_factory.standard_tools() + tools_factory.guardrail_tools(),
#     topic="news summarization",
#     custom_instructions=news_assistant_instructions,
# )

# Function to interact with the agent and get news summarization
