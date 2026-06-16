# ReAct Agent Architecture: Agentic Brand Toolkit

This document explains the technical implementation of the ReAct (Reasoning and Acting) agent architecture used in the Agentic Brand Toolkit. It details what was refactored, how the dynamic orchestration works, and why specific design decisions were made.

---

## 1. The Paradigm Shift: From Pipeline to Agent

### **Before: The Fixed Workflow Pipeline**
Originally, the project relied on a static, developer-defined `StateGraph` pipeline. Execution moved linearly from node to node:
`Crawl -> Visual Identity -> Brand Profile -> Competitor Discovery -> ... -> Toolkit Builder`

While this worked reliably, it was completely rigid. The execution path could not dynamically adjust to missing information or intelligently recover from mid-stream changes.

### **After: The ReAct Agent Architecture**
The orchestration has been completely decoupled from the execution logic. We transitioned to a **ReAct (Reasoning + Acting)** framework using LangGraph and Langchain's Google GenAI integrations. 

Now, the LLM (`gemini-2.5-flash`) acts as the **Brain**. It is given a list of available tools, told the final objective (building a Brand Toolkit), and dynamically decides the execution order. It reasons about what information is missing, takes action by calling a specific tool, observes the result, and loops until the toolkit is complete.

---

## 2. Core Components of the Agent System

The architecture is built upon three primary pillars: State, Tools, and the Orchestrator.

### A. The Agent State (`agent_state.py`)
The system requires a continuously updating memory object. We created an `AgentState` that inherits your original `BrandState` schemas but includes LangGraph's native `messages` property. 
- **Why?** The `messages` array maintains the strict conversational turn history (Human -> AI -> Tool) required by Gemini, while the other fields (`website_content`, `brand_profile`, etc.) hold the heavy JSON and text payloads.

### B. The Tool Layer (`src/application/tools/`)
We wrapped every existing business logic `Service` into an explicit Langchain tool.
- **The Context Window Problem:** Naively returning tool outputs (like a full website HTML scrape or massive competitor profiles) directly into the LLM's conversation trace would instantly blow up Gemini's context window and cause catastrophic token limits.
- **The Solution:** The `BrandTool` interface intercepts the execution. When a tool like `CrawlTool` finishes, it saves the giant data payload directly into the `AgentState` (e.g., `state["website_content"] = HTML`), and returns a tiny, concise string back to the LLM (e.g., *"Successfully crawled the website. Content is in memory."*). 

This allows the LLM to know the action succeeded without being blinded by thousands of lines of code.

### C. The Orchestrator (`brand_intelligence_agent.py`)
The `BrandIntelligenceAgent` is a custom two-node LangGraph:
1. **`agent_node`**: This is where Gemini "thinks". 
   - We dynamically construct a `SystemMessage` on every loop. This message evaluates the `AgentState` and literally prints out a checklist of what is `"Present"` and what is `"Missing"` (e.g., `- brand_profile: Missing`).
   - The LLM reads this checklist, consults tool descriptions, and outputs a `tool_call`.
2. **`tools_node`**: This executes the requested Python functions. It maps the tool name requested by the LLM to the actual `BrandTool` instance, executes it, catches any errors, and appends the success/failure message back to the LLM's history.

---

## 3. Advanced Resilience: Rate Limit Handling

A significant challenge in autonomous agents operating on Free-Tier APIs is encountering `429 RESOURCE_EXHAUSTED` rate limits. Because an agent loop might make 15-20 heavy LLM calls sequentially, rate limits are inevitable.

### **How it's handled:**
Both the deep `GeminiAdapter` (used by the services) and the overarching `_agent_node` (used for reasoning) implement robust, state-aware failover mechanisms:
- We load an array of comma-separated `GEMINI_API_KEY`s from the `.env` file.
- When `_agent_node` attempts to "think" and receives a `429` error, the `except` block catches it.
- It immediately cycles to the next API key in the array.
- It seamlessly re-instantiates `ChatGoogleGenerativeAI`, re-binds the tools, pauses for a moment, and retries the exact same prompt.
- **Why this matters:** The pipeline does not crash. The graph state remains perfectly intact, allowing the agent to wait out quotas or switch accounts seamlessly without losing 10 minutes of prior analysis.

---

## 4. Execution Trace Example

When you run `main.py`, here is what is happening under the hood:

1. **Initialization**: The initial `HumanMessage` is injected: *"Please build a brand toolkit for drinklucent.com."*
2. **Turn 1 (Reasoning)**: The LLM reads the System Prompt. It sees all artifacts are `Missing`. It reads tool descriptions and realizes `crawl_website` must be used first. It issues a tool call.
3. **Turn 1 (Action)**: The `tools_node` runs `CrawlTool`. It extracts the HTML, saves it to `state["website_content"]`, and replies to the LLM: *"Success."*
4. **Turn 2 (Reasoning)**: The LLM reads the updated System Prompt. It sees `website_content: Present`. It decides it can now run both `extract_visual_identity` and `generate_brand_profile` simultaneously.
5. **Turn N**: This loop continues. If a tool fails, the error is fed back to the LLM, which can decide to retry or try a different approach.
6. **Termination**: Once all checklists read `Present`, the LLM calls `build_final_toolkit`. The graph recognizes this as the termination condition and saves the structured artifacts to disk.
