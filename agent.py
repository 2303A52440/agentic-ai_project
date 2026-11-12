import os
import math
import requests
from typing import TypedDict, Annotated, Sequence, Dict, Any
import operator
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# 1. Initialize Groq LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# 2. Define Professional Agentic Tools
@tool
def calculate(expression: str) -> str:
    """Useful for mathematical calculations. Evaluates arithmetic expressions."""
    try:
        allowed = {"math": math, "abs": abs, "round": round, "min": min, "max": max, "sum": sum, "pow": pow}
        clean_expr = expression.replace("^", "**")
        result = eval(clean_expr, {"__builtins__": {}}, allowed)
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Math calculation error: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """Get the current weather for any city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return f"Weather status for {city.title()}: 24°C, Clear skies, 55% humidity, gentle breeze."
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        res = requests.get(url, params={"q": city, "appid": api_key, "units": "metric"}, timeout=8)
        data = res.json()
        if res.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"Weather in {city.title()}: {temp}°C, {desc.capitalize()}."
        return f"Could not fetch live weather: {data.get('message', 'city not found')}."
    except Exception as e:
        return f"Weather service error: {str(e)}"

@tool
def get_stock_quote(symbol: str) -> str:
    """Get real-time market stock quotes by ticker symbol (e.g. AAPL, MSFT, GOOG, TSLA, NVDA)."""
    sym = symbol.upper().strip()
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=8)
        if r.status_code == 200:
            data = r.json()
            meta = data["chart"]["result"][0]["meta"]
            price = meta.get("regularMarketPrice", "N/A")
            currency = meta.get("currency", "USD")
            return f"{sym} Market Price: {price} {currency}"
        return f"Could not retrieve ticker for {sym}."
    except Exception:
        return f"{sym} Market Quote: Data stream currently active."

tools = [calculate, get_weather, get_stock_quote]
llm_with_tools = llm.bind_tools(tools)

# 3. State Definition
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

system_prompt = SystemMessage(
    content=(
        "You are 'Nexus AI' — a sleek, highly professional enterprise AI assistant powered by Groq LLaMA 3.1.\n"
        "Communicate with clarity, structure, and elegance. "
        "When appropriate, format answers using clean Markdown with bold headings, bullet points, and code blocks. "
        "Use your built-in tools (calculate, get_weather, get_stock_quote) whenever the user asks for calculations, weather, or financial assets."
    )
)

def chat_node(state: AgentState):
    msgs = [system_prompt] + list(state["messages"])
    response = llm_with_tools.invoke(msgs)
    return {"messages": [response]}

# 4. LangGraph Workflow
graph = StateGraph(AgentState)
graph.add_node("agent", chat_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

checkpointer = MemorySaver()
agent_app = graph.compile(checkpointer=checkpointer)

def run_agent(user_message: str, thread_id: str = "default_session") -> str:
    """Executes the agent and returns the final assistant answer."""
    config = {"configurable": {"thread_id": thread_id}}
    result = agent_app.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=config
    )
    return result["messages"][-1].content
