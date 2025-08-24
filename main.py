from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from teams.travel_team import team
import asyncio
import json

def format_travel_content(content):
    """Format travel search results for better readability"""
    try:
        # Handle list type content (function calls and results)
        if isinstance(content, list):
            if len(content) > 0:
                first_item = str(content[0])
                if 'FunctionCall(' in first_item:
                    return "🔍 Searching for travel information..."
                elif 'FunctionExecutionResult(' in first_item:
                    return ""  # Hide raw function execution results
            return ""
        
        # Handle string content
        if isinstance(content, str):
            # Check if it's raw dictionary content that needs formatting
            if (content.strip().startswith('{') and "'query':" in content) or \
               (content.strip().startswith("{'query'")) or \
               ("'follow_up_questions'" in content and "'answer':" in content):
                try:
                    # Try to safely evaluate the string as a Python dictionary
                    data = eval(content)
                    if isinstance(data, dict) and 'query' in data:
                        return format_search_result(data)
                except Exception:
                    # If eval fails, return empty to hide malformed dictionary strings
                    return ""
            
            # Return regular text content as-is
            return content
        
        # If content is a dict/object, format it
        if hasattr(content, 'get') or isinstance(content, dict):
            return format_search_result(content)
            
        return str(content)
    except Exception as e:
        return str(content)

def format_search_result(data):
    """Format a single search result"""
    if not isinstance(data, dict):
        return str(data)
    
    formatted = []
    
    # Add query and answer
    if 'query' in data:
        formatted.append(f"🔍 Search Query: {data['query']}")
    
    if 'answer' in data:
        formatted.append(f"📋 Summary: {data['answer']}")
    
    # Add top results with better formatting
    if 'results' in data and data['results']:
        formatted.append("\n📍 Top Recommendations:")
        for i, result in enumerate(data['results'][:3], 1):
            if isinstance(result, dict):
                title = result.get('title', 'No title')
                content = result.get('content', '')
                # Truncate content for readability
                if len(content) > 200:
                    content = content[:200] + "..."
                formatted.append(f"\n   {i}. {title}")
                if content:
                    formatted.append(f"      {content}")
    
    return '\n'.join(formatted)

async def main():
    print("🌍 Welcome to Travel Planner!")
    print("=" * 50)
    
    task = TextMessage(content="Plan a trip to Paris for 5 days.", source="User")
    
    async for message in team.run_stream(task=task):
        if isinstance(message, TaskResult):
            print(f"\n✅ Task completed: {message.stop_reason}")
        else:
            # Show raw content for debugging
            print(f"\n🔍 RAW CONTENT ({message.source}):")
            print(f"Type: {type(message.content)}")
            print(f"Content: {repr(message.content)}")
            print("=" * 80)
            
            # Format the message content for better readability
            formatted_content = format_travel_content(message.content)
            
            # Show formatted content
            if formatted_content.strip():
                print(f"\n📝 FORMATTED CONTENT ({message.source}):")
                print(f"{formatted_content}")
            else:
                print(f"\n📝 FORMATTED CONTENT ({message.source}): [HIDDEN/EMPTY]")
                
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())