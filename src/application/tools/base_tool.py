from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from pydantic import BaseModel

class BrandTool(ABC):
    name: str
    description: str
    args_schema: Type[BaseModel]

    @abstractmethod
    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the tool and returns state updates.
        Must return a dictionary containing keys to update in the AgentState.
        Must include a 'tool_message' key with the string content to return to the LLM.
        """
        pass
