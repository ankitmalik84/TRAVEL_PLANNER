from autogen_agentchat.agents import AssistantAgent
from models.openAIModel import model_client
from utils.tools import create_travel_specific_search_tool

# Create the travel-specific search tool
travel_search_tool = create_travel_specific_search_tool()

planner_agent = AssistantAgent(
    name="Travel_Planner",
    description="A travel planner agent that helps users plan their trips using real-time travel information.",
    model_client=model_client,
    tools=[travel_search_tool],
    system_message="You are a travel planner agent. Your task is to help users plan their trips by providing information about destinations, itineraries, and travel tips. Use the travel search tool to find current information about hotels, restaurants, attractions, events, and travel conditions to create comprehensive and up-to-date travel plans.",
)