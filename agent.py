import os
import math
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

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq with high-speed 120B model (or fallback to 20B)
try:
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        api_key=GROQ_API_KEY
    )
except Exception:
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        api_key=GROQ_API_KEY
    )


# ========================================================
# Clinical & Medical Intelligence Tools
# ========================================================

@tool
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """Calculates Body Mass Index (BMI), category, and healthy target weight range."""
    try:
        height_m = height_cm / 100.0
        bmi = round(weight_kg / (height_m ** 2), 1)
        
        if bmi < 18.5:
            cat = "Underweight"
        elif 18.5 <= bmi < 24.9:
            cat = "Normal weight (Healthy range)"
        elif 25.0 <= bmi < 29.9:
            cat = "Overweight"
        else:
            cat = "Obese (Consult a healthcare provider)"

        ideal_min = round(18.5 * (height_m ** 2), 1)
        ideal_max = round(24.9 * (height_m ** 2), 1)

        return (
            f"BMI Assessment:\n"
            f"- Calculated BMI: {bmi}\n"
            f"- Classification: {cat}\n"
            f"- Recommended Weight Range for {height_cm}cm: {ideal_min} kg – {ideal_max} kg\n"
            f"- Recommended Daily Water Intake: ~{round(weight_kg * 0.033, 1)} Liters"
        )
    except Exception as e:
        return f"BMI Calculation error: {str(e)}"


@tool
def emergency_triage_checker(symptoms: str) -> str:
    """Checks for clinical red flags and critical emergency indicators."""
    critical_triggers = [
        "chest pain", "shortness of breath", "difficulty breathing",
        "stroke", "facial drooping", "arm weakness", "slurred speech",
        "loss of consciousness", "coughing blood", "anaphylaxis",
        "severe allergic reaction", "sudden numbness", "poisoning"
    ]
    s_lower = symptoms.lower()
    matched = [c for c in critical_triggers if c in s_lower]

    if matched:
        return (
            "🚨 CRITICAL EMERGENCY ALERT:\n"
            f"The reported symptoms contain high-risk red flags ({', '.join(matched)}).\n"
            "Action Required: Immediately call emergency services (911 in the US/Canada, 112 in Europe, 102/108 in India) "
            "or proceed to the nearest emergency room. Do not drive yourself."
        )
    return "Triage Status: No immediate acute life-threatening emergency flags detected in query keywords. Proceed with clinical assessment."


@tool
def clinical_calculator(expression: str) -> str:
    """Evaluates medical and dosage calculations accurately."""
    try:
        allowed = {"math": math, "abs": abs, "round": round, "min": min, "max": max}
        clean = expression.replace("^", "**")
        result = eval(clean, {"__builtins__": {}}, allowed)
        return f"Calculation Result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"


tools = [calculate_bmi, emergency_triage_checker, clinical_calculator]
llm_with_tools = llm.bind_tools(tools)


# ========================================================
# LangGraph Workflow Architecture
# ========================================================

class MedicalState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


medical_system_prompt = SystemMessage(
    content=(
        "You are 'MediCare AI', an advanced, clinical-grade medical intelligence assistant powered by Groq.\n"
        "Your mission is to provide accurate, empathetic, and evidence-based health guidance.\n\n"
        "Always structure your clinical responses with clean Markdown sections:\n"
        "### 🩺 Symptom & Clinical Assessment\n"
        "### 🔍 Possible Causes & Risk Factors\n"
        "### 💡 Evidence-Based Self-Care & Recovery Steps\n"
        "### 🚨 Red Flags (When to Seek Immediate Emergency Care)\n"
        "### ⚠️ Clinical Disclaimer\n"
        "*(Always state: 'This AI consultation is for informational triage only and does not replace a physical examination, formal diagnosis, or prescription by a licensed physician.')*\n\n"
        "Use your tools (emergency_triage_checker, calculate_bmi, clinical_calculator) whenever appropriate."
    )
)


def medical_chat_node(state: MedicalState):
    msgs = [medical_system_prompt] + list(state["messages"])
    response = llm_with_tools.invoke(msgs)
    return {"messages": [response]}


graph = StateGraph(MedicalState)
graph.add_node("agent", medical_chat_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

checkpointer = MemorySaver()
medical_agent_app = graph.compile(checkpointer=checkpointer)


def run_medical_agent(user_message: str, thread_id: str = "patient_session") -> str:
    """Executes the medical agent and returns the structured clinical response."""
    config = {"configurable": {"thread_id": thread_id}}
    result = medical_agent_app.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=config
    )
    return result["messages"][-1].content
