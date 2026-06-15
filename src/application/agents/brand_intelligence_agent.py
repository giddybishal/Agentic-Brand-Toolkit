from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool

import os
from dotenv import load_dotenv

from .agent_state import AgentState
from ..tools.base_tool import BrandTool

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
        self.graph = self._build_graph()

    def _get_dummy_func(self):
        def dummy(**kwargs):
            pass
        return dummy

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", self._tools_node)
        
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        workflow.add_edge("tools", "agent")
        return workflow.compile()

    def _agent_node(self, state: AgentState) -> Dict[str, Any]:
        messages = state.get("messages", [])
        new_messages = []
        
        sys_msg = self._build_system_message(state)
        
        if not messages:
            url = state.get("website_url", "")
            initial_msg = HumanMessage(content=f"Please build a brand toolkit for {url}. You must use tools to discover and generate all necessary assets.")
            messages = [initial_msg]
            new_messages.append(initial_msg)
            
        print("[*] Agent thinking...")
        
        import time
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
            print(f"    Agent says: {response.content}")
        for tc in response.tool_calls:
            print(f"    Agent requesting tool: {tc['name']}")
            
        return {"messages": new_messages}

    def _should_continue(self, state: AgentState) -> str:
        messages = state.get("messages", [])
        last_message = messages[-1]
        
        if getattr(last_message, "tool_calls", None):
            return "continue"
            
        return "end"

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
                    result = tool_instance.execute(state, args)
                    tool_msg_content = result.pop("tool_message", f"Tool {tool_name} executed successfully.")
                    
                    updates.update(result)
                    tool_messages.append(ToolMessage(content=tool_msg_content, tool_call_id=tool_call["id"]))
                except Exception as e:
                    print(f"[!] Tool {tool_name} failed: {e}")
                    tool_messages.append(ToolMessage(content=f"Error executing {tool_name}: {str(e)}", tool_call_id=tool_call["id"]))
            else:
                tool_messages.append(ToolMessage(content=f"Tool {tool_name} not found.", tool_call_id=tool_call["id"]))
                
        updates["messages"] = tool_messages
        return updates

    def _build_system_message(self, state: AgentState) -> SystemMessage:
        status = [
            f"- website_content: {'Present' if state.get('website_content') else 'Missing'}",
            f"- visual_identity: {'Present' if state.get('visual_identity') else 'Missing'}",
            f"- brand_profile: {'Present' if state.get('brand_profile') else 'Missing'}",
            f"- competitors: {'Present' if state.get('competitors') else 'Missing'}",
            f"- competitor_profiles: {'Present' if state.get('competitor_profiles') else 'Missing'}",
            f"- brand_social_profile: {'Present' if state.get('brand_social_profile') else 'Missing'}",
            f"- competitor_social_profiles: {'Present' if state.get('competitor_social_profiles') else 'Missing'}",
            f"- engagement_metrics: {'Present' if state.get('engagement_metrics') else 'Missing'}",
            f"- gap_analysis: {'Present' if state.get('gap_analysis') else 'Missing'}",
            f"- growth_strategy: {'Present' if state.get('growth_strategy') else 'Missing'}",
            f"- creator_guidelines: {'Present' if state.get('creator_guidelines') else 'Missing'}",
            f"- toolkit: {'Present' if state.get('toolkit') else 'Missing'}"
        ]
        status_str = "\n".join(status)
        
        content = f"""You are the Brand Intelligence Agent. Your goal is to construct a comprehensive Brand Toolkit for the user's website.
You control the execution flow by selecting which tool to call next based on what information is currently missing.

Current State Status:
{status_str}

Instructions:
1. Review the Current State Status above.
2. Identify what is missing.
3. Call the appropriate tool to generate the missing information.
4. Do NOT call the same tool more than once unless it failed.
5. You MUST call `build_final_toolkit` as the very last step once everything else is Present.
6. Once `build_final_toolkit` is called, you are done.

Only respond with tool calls. Do not try to generate the brand profile or other assets directly in text. Always use the provided tools.
You can call multiple tools in parallel if their inputs are already Present.
"""
        return SystemMessage(content=content)
