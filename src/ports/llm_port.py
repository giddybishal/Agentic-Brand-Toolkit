from abc import ABC, abstractmethod
from typing import Type, TypeVar, Any

T = TypeVar('T')

class LLMPort(ABC):
    @abstractmethod
    def generate_structured_data(self, prompt: str, schema: Type[T]) -> T:
        pass
