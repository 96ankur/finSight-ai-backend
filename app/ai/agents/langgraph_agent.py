# app/agents/langgraph_agent.py

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from ..prompts.agent_prompt import agent_prompt
from app.utils.agent_util import parse_agent_output
from ..tools.tool_registry import ToolRegistry

# pass llm from outside (important)
class AgentState(TypedDict):
    input: str
    messages: List
    tool_name: Optional[str]
    tool_input: Optional[dict]
    tool_result: Optional[str]
    final_answer: Optional[str]
    step_count: int
    last_tool: Optional[str]


# -------------------------
# DECISION NODE
# -------------------------
async def decision_node(state: AgentState, llm):
    decision_chain = agent_prompt | llm

    decision = await decision_chain.ainvoke({
        "input": state["input"],
        "history": state["messages"]
    })

    parsed = parse_agent_output(decision.content)

    return {
        "tool_name": parsed.get("tool"),
        "tool_input": parsed.get("input"),
        "final_answer": parsed.get("answer")
    }


# -------------------------
# TOOL NODE
# -------------------------
def tool_node(state: AgentState, user_id: str):
    tool_name = state.get("tool_name")
    tool_input = state.get("tool_input")

    if not tool_name or tool_name == "none":
        return state

    registry = ToolRegistry.for_user(user_id)
    tool_entry = registry.get_tool(tool_name)

    if not tool_entry:
        return {"final_answer": f"Tool {tool_name} not found"}

    tool = tool_entry["tool"]
    input_model = tool_entry["input_model"]

    try:
        structured_input = input_model(**tool_input)
        result = tool.run(structured_input).result
    except Exception as e:
        result = f"ERROR: {str(e)}"

    return {
        "tool_result": result,
        "step_count": state["step_count"] + 1,
        "messages": state["messages"] + [
            HumanMessage(
                content=f"""
                Tool Used: {tool_name}
                Result: {result}
                """
            )
        ]
    }


# -------------------------
# ROUTING LOGIC
# -------------------------
def should_continue(state: AgentState):
    if state.get("tool_name") == "none":
        return "end"

    if state.get("tool_name") == state.get("last_tool"):
        return "end"
    
    if state.get("step_count", 0) > 3:
        return "end"

    return "continue"


# -------------------------
# GRAPH BUILDER
# -------------------------
def build_graph(llm, user_id: str):
    builder = StateGraph(AgentState)

    # wrap nodes to inject dependencies
    async def decision_wrapper(state):
        return await decision_node(state, llm)

    def tool_wrapper(state):
        return tool_node(state, user_id)

    builder.add_node("decision", decision_wrapper)
    builder.add_node("tool", tool_wrapper)

    builder.set_entry_point("decision")

    builder.add_conditional_edges(
        "decision",
        should_continue,
        {
            "continue": "tool",
            "end": END
        }
    )

    builder.add_edge("tool", "decision")

    return builder.compile()


# -------------------------
# RUN FUNCTION
# -------------------------
async def run_agent(llm, user_id: str, user_input: str):
    graph = build_graph(llm, user_id)

    result = await graph.ainvoke({
        "input": user_input,
        "messages": [],
        "step_count": 0
    })

    if result.get("final_answer"):
        return result["final_answer"]

    return result.get("tool_result", "No response")