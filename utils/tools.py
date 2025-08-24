import os
from typing import List, Dict, Any
from langchain_tavily import TavilySearch
from autogen_ext.tools.langchain import LangChainToolAdapter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_travel_specific_search_tool() -> LangChainToolAdapter:
    """
    Create a travel-specific search tool with customized instructions
    
    Returns:
        LangChainToolAdapter: Wrapped Tavily search tool optimized for travel queries
    """
    # Create a custom Tavily tool with travel-focused configuration
    travel_search_tool = TavilySearch(
        max_results=3,
        include_answer=True,
        include_raw_content=False,
        include_images=False,
        name="travel_search",
        description="Search for travel-related information including destinations, hotels, restaurants, attractions, and travel tips. Use this for real-time travel information and recommendations."
    )
    
    # Wrap for AutoGen
    autogen_travel_tool = LangChainToolAdapter(travel_search_tool)
    
    return autogen_travel_tool
