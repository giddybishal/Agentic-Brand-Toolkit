from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.types import interrupt
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool

import os
from dotenv import load_dotenv
import json
import time

from .agent_state import AgentState
from ..tools.base_tool import BrandTool
from ...utils.logger import log_event

class BrandIntelligenceAgent:
    def __init__(self, tools: List[BrandTool]):
        self.brand_tools = {tool.name: tool for tool in tools}
        
        load_dotenv()
        keys_str = os.getenv("GEMINI_API_KEY", "")
        self.api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        self.current_key_idx = 0
        api_key = self.api_keys[self.current_key_idx] if self.api_keys else None
        
        # Using gemini-2.5-flash as the orchestrator LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.2,
            api_key=api_key
        )
        
        # Convert our custom BrandTools to Langchain StructuredTools for LLM tool binding
        self.lc_tools = [
            StructuredTool.from_function(
                func=self._get_dummy_func(),
                name=tool.name,
                description=tool.description,
                args_schema=tool.args_schema,
            )
            for tool in tools
        ]
        self.llm_with_tools = self.llm.bind_tools(self.lc_tools)
        
        serde = JsonPlusSerializer(
            allowed_msgpack_modules=[
                ("src.domain.models.visual_identity", "VisualIdentity"),
                ("src.domain.models.brand_profile", "BrandProfile"),
                ("src.domain.models.creator_guidelines", "CreatorGuidelines"),
                ("src.domain.models.brand_toolkit", "BrandToolkit"),
                ("src.domain.models.competitor", "Competitor"),
                ("src.domain.models.competitor", "CompetitorProfile"),
                ("src.domain.models.social_media", "SocialMediaProfile"),
                ("src.domain.models.analytics", "EngagementMetrics"),
                ("src.domain.models.analytics", "GapAnalysis"),
                ("src.domain.models.analytics", "GrowthStrategy")
            ]
        )
        self.checkpointer = MemorySaver(serde=serde)
        self.graph = self._build_graph()

    def _get_dummy_func(self):
        def dummy(**kwargs):
            pass
        return dummy

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", self._tools_node)
        workflow.add_node("final_review", self._final_review_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "final_review": "final_review"
            }
        )
        workflow.add_edge("tools", "agent")
        workflow.add_conditional_edges(
            "final_review",
            lambda s: "end" if s.get("final_review_approved") else "agent",
            {"end": END, "agent": "agent"}
        )
        return workflow.compile(checkpointer=self.checkpointer)

    def _build_system_message(self, state: AgentState) -> SystemMessage:
        status_checks = {}
        for k in ["website_url", "visual_identity", "brand_profile", "competitors", "competitor_profiles", "brand_social_profile", "engagement_metrics", "gap_analysis", "growth_strategy", "creator_guidelines"]:
            val = state.get(k)
            if val:
                try:
                    if hasattr(val, "model_dump"):
                        val_str = json.dumps(val.model_dump())
                    elif isinstance(val, list) and len(val) > 0 and hasattr(val[0], "model_dump"):
                        val_str = json.dumps([v.model_dump() for v in val])
                    else:
                        val_str = json.dumps(val)
                except Exception:
                    val_str = str(val)
                
                if len(val_str) > 3000:
                    val_str = val_str[:3000] + "... [TRUNCATED]"
                status_checks[k] = f"Present. Data: {val_str}"
            else:
                status_checks[k] = "Missing"
                
        # Handle massive payloads separately to avoid context bloat
        status_checks["website_content"] = "Present" if state.get("website_content") else "Missing"
        status_checks["toolkit"] = "Present" if state.get("toolkit") else "Missing"
        
        status_lines = "\n".join([f"- {k}: {v}" for k, v in status_checks.items()])
        query = state.get("query", "No query provided.")
        
        sys_msg = f"""You are an elite, Role-Aware, Intent-Driven Brand Intelligence Assistant.
        
Your purpose is to answer the user's natural language queries about brands using a precise set of analytical tools.

USER QUERY: "{query}"

=== OUTPUT MODES & INTENT ===
Analyze the user's query and implicitly determine their role and intent. Map it to one of the following output modes:
- MODE 1 (BRAND_SUMMARY): User wants a general overview or HR culture info. Execute ONLY tools needed for brand profile.
- MODE 2 (VISUAL_IDENTITY_ONLY): User (Designer) wants colors, fonts, or logos. Execute ONLY visual extraction tools.
- MODE 3 (COMPETITOR_INSIGHT): User (Marketing) wants to compare competitors. Execute ONLY competitor tools.
- MODE 4 (STRATEGY_ANALYSIS): User wants growth/gap analysis. Execute ONLY analytics/strategy tools.
- MODE 5 (FULL_TOOLKIT): User explicitly asks to "generate full brand toolkit" or "run full pipeline".

=== MINIMAL TOOL EXECUTION POLICY ===
- "Use the smallest possible set of tools required to answer the question."
- Do NOT run the full pipeline unless explicitly requested.
- Always check the Current State below. If a required dependency is already "Present", DO NOT call the tool that produces it.
- Never invent URLs. If `website_url` is Missing, you MUST call `resolve_brand_identity` first.

=== CURRENT STATE ===
{status_lines}

=== EXECUTION RULES ===
1. Only call tools whose dependencies are met (check tool descriptions).
2. Once the necessary tools have run and the Current State contains the exact data you need (e.g. visual_identity data is "Present" and contains the color hex codes), STOP CALLING TOOLS.
3. Your final output MUST NOT BE A TOOL CALL. Your final output must be a helpful, cleanly formatted conversational response summarizing the extracted data from the State to answer the user's query exactly.
4. DO NOT hallucinate. If the state data is missing or extraction failed, truthfully state that you do not have the information.
"""
        return SystemMessage(content=sys_msg)

    def _agent_node(self, state: AgentState) -> Dict[str, Any]:
        log_event("GRAPH", {"Current Node": "agent", "Messages Count": len(state.get("messages", []))})
        
        updates = {}
        
        if state.get("resolved_url") and not state.get("human_approved_url"):
            log_event("HITL", {"Reason": "Mandatory URL Validation", "Confidence": state.get("resolution_confidence"), "URL": state["resolved_url"]})
            human_feedback = interrupt(f"Please review the resolved URL: {state['resolved_url']} (Confidence: {state.get('resolution_confidence')}). Enter 'approve' to proceed, or provide the correct URL: ")
            
            new_url = state["resolved_url"]
            if human_feedback and human_feedback.lower() not in ["approve", "y", "yes"]:
                new_url = human_feedback.strip()
            
            log_event("HITL", {"Action": "URL Approved/Updated", "New URL": new_url})
            updates.update({"website_url": new_url, "resolved_url": new_url, "human_approved_url": True})
            
            # Update local state dictionary to ensure immediate LLM prompts have the correct data
            state["website_url"] = new_url
            state["resolved_url"] = new_url
            state["human_approved_url"] = True

        messages = state.get("messages", [])
        new_messages = []
        
        sys_msg = self._build_system_message(state)
        
        if not messages:
            query = state.get("query", "Please assist me with brand analysis.")
            initial_msg = HumanMessage(content=query)
            messages = [initial_msg]
            new_messages.append(initial_msg)
            
        log_event("AGENT", {"Goal": "Analyzing User Request", "Action": "Thinking"})
        
        max_retries = max(3, len(self.api_keys) * 2) if getattr(self, "api_keys", None) else 3
        retries = 0
        
        while retries < max_retries:
            try:
                response = self.llm_with_tools.invoke([sys_msg] + messages)
                break
            except Exception as e:
                error_msg = str(e).lower()
                print(f"[!] Agent LLM error (attempt {retries + 1}/{max_retries}): {e}")
                
                if "429" in error_msg or "resource_exhausted" in error_msg or "quota" in error_msg:
                    if hasattr(self, "api_keys") and len(self.api_keys) > 1:
                        self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
                        print(f"    Rate limit hit in Agent! Switching to API key #{self.current_key_idx + 1}/{len(self.api_keys)}...")
                        self.llm = ChatGoogleGenerativeAI(
                            model="gemini-2.5-flash", 
                            temperature=0.2,
                            api_key=self.api_keys[self.current_key_idx]
                        )
                        self.llm_with_tools = self.llm.bind_tools(self.lc_tools)
                        time.sleep(1)
                    else:
                        time.sleep(2 ** retries)
                elif "503" in error_msg or "unavailable" in error_msg:
                    time.sleep(2 ** retries)
                else:
                    time.sleep(2 ** retries)
                    
                retries += 1
                if retries >= max_retries:
                    raise
                    
        new_messages.append(response)
        
        if response.content:
            if isinstance(response.content, list):
                content_str = " ".join([item.get("text", "") for item in response.content if isinstance(item, dict) and "text" in item])
                print(f"    Agent says: {content_str}")
            else:
                print(f"    Agent says: {response.content}")
                
        for tc in response.tool_calls:
            print(f"    Agent requesting tool: {tc['name']}")
            
        updates["messages"] = new_messages
        return updates

    def _should_continue(self, state: AgentState) -> str:
        messages = state.get("messages", [])
        last_message = messages[-1]
        
        if getattr(last_message, "tool_calls", None):
            return "continue"
            
        return "final_review"

    def _final_review_node(self, state: AgentState) -> Dict[str, Any]:
        log_event("GRAPH", {"Current Node": "final_review"})
        if not state.get("final_review_approved"):
            log_event("HITL", {"Reason": "Final Review Checkpoint"})
            human_feedback = interrupt("Agent has gathered enough information and is ready to generate the final response. Enter 'approve' to finalize, or provide additional instructions: ")
            
            if human_feedback and human_feedback.lower() not in ["approve", "y", "yes"]:
                log_event("HITL", {"Action": "More work requested by user", "Feedback": human_feedback})
                return {"messages": [HumanMessage(content=f"Human feedback: {human_feedback}")]}
            
            log_event("HITL", {"Action": "Final review approved"})
            return {"final_review_approved": True}
        return {}

    def _tools_node(self, state: AgentState) -> Dict[str, Any]:
        messages = state.get("messages", [])
        last_message = messages[-1]
        
        updates = {}
        tool_messages = []
        
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            args = tool_call["args"]
            
            tool_instance = self.brand_tools.get(tool_name)
            if tool_instance:
                try:
                    log_event("TOOL", {"Tool": tool_name, "Inputs": args})
                    result = tool_instance.execute(state, args)
                    tool_msg_content = result.pop("tool_message", f"Tool {tool_name} executed successfully.")
                    
                    log_event("STATE", {"Updated": list(result.keys())})
                    updates.update(result)
                    tool_messages.append(ToolMessage(content=tool_msg_content, tool_call_id=tool_call["id"]))
                except Exception as e:
                    print(f"[!] Tool {tool_name} failed: {e}")
                    tool_messages.append(ToolMessage(content=f"Error executing {tool_name}: {str(e)}", tool_call_id=tool_call["id"]))
            else:
                tool_messages.append(ToolMessage(content=f"Tool {tool_name} not found.", tool_call_id=tool_call["id"]))
                
        updates["messages"] = tool_messages
        return updates
