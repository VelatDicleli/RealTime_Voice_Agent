from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model="openai/gpt-oss-20b",
    max_tokens=1024
)

def retrieve_data_from_vector_store(query: str) -> str:
    """Retrieve data from a specified vector store based on the query."""
    return

def append_sheets_row(data: dict) -> str:
    """Append a row to a Google Sheets document."""
    return

def weather_info(location: str) -> str:
    """Get the current weather information for a given location."""
    return

def email_send(subject: str, body: str) -> str:
    """send email to given user, no receiver specified."""
    return

def calendar_create(start: str, end: str) -> str:
    """Create a calendar event."""
    return

tools = [retrieve_data_from_vector_store, weather_info,email_send,calendar_create, append_sheets_row]

system_prompt = """You are a helpful assistant that uses the following tools to help users with their requests."""

memory = InMemorySaver()

agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=system_prompt,
    checkpointer=memory,
)

agent_config = {"configurable": {"thread_id": "default_user"}}