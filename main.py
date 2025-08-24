from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from teams.travel_team import team
import asyncio

async def main():
    task = TextMessage(content="Plan a trip to Paris for 5 days.",source="User")
    async for message in team.run_stream(task=task):
        if isinstance(message,TaskResult):
                message = f'Interview completed with result: {message.stop_reason}'
                print(message)
        else:
                message = f'{message.source}: {message.content}'
                print(message)


if __name__ == "__main__":
    asyncio.run(main())