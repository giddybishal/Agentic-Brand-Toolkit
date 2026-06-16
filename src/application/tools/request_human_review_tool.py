from typing import Dict, Any
from pydantic import BaseModel, Field
from .base_tool import BrandTool

class RequestHumanReviewToolSchema(BaseModel):
    reason: str = Field(description="The reason why human review is being requested (e.g., 'ambiguous competitors', 'low confidence in target audience').")
    context_to_review: str = Field(description="The specific information or context you want the human to review.")
    confidence_score: float = Field(description="The agent's confidence score (0.0 to 1.0) regarding the current data.")

class RequestHumanReviewTool(BrandTool):
    name = "request_human_review"
    description = """
    Dependency:
    - Requires: Uncertainty or low confidence in intermediate results.
    - Produces: Direct human feedback/approval.
    
    Rule: Use this tool whenever your confidence is low (e.g., < 0.7) regarding:
    - Ambiguous competitors.
    - Weak crawl results.
    - Conflicting brand signals.
    - Uncertain positioning.
    - Unclear social recommendations.
    
    This tool pauses execution and asks the user for clarification or guidance.
    """
    args_schema = RequestHumanReviewToolSchema

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        reason = args.get("reason", "Uncertainty")
        context_to_review = args.get("context_to_review", "")
        confidence = args.get("confidence_score", 0.0)
        
        # We don't call interrupt() here directly if we're not inside a LangGraph node that supports it,
        # but in langgraph, `interrupt()` from `langgraph.types` CAN be called from anywhere within the graph's execution thread.
        # However, to be safe and compatible with earlier langgraph versions, we will use langgraph.types.interrupt
        
        from langgraph.types import interrupt
        
        print(f"[*] Tool executing: Requesting human review. Reason: {reason} (Confidence: {confidence})")
        
        # Pause and ask human for feedback
        human_feedback = interrupt(
            f"HUMAN REVIEW REQUESTED:\nReason: {reason}\nConfidence: {confidence}\nContext: {context_to_review}\n\nPlease provide your feedback/clarification: "
        )
        
        return {
            "tool_message": f"Human Feedback Received: {human_feedback}"
        }
