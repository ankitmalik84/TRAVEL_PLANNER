from autogen_agentchat.teams import RoundRobinGroupChat

# Agents
from agents.planner import planner_agent
from agents.researcher import research_agent

from config.settings import TERMINATION_WORD
from utils.utils import get_termination_condition

team = RoundRobinGroupChat(
    participants=[planner_agent, research_agent],
    name="Travel Planning Team",
    description="A collaborative team that helps users plan their trips by researching destinations, creating itineraries, and providing travel tips. The team consists of a planner agent and a research agent working together in a round-robin fashion.",
    termination_condition=get_termination_condition()
)