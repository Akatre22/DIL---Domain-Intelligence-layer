from __future__ import annotations

from typing import Any, Dict, List, Protocol


class LLMCallable(Protocol):
    """Protocol for LLM adapter callables."""

    def __call__(self, messages: List[Dict[str, str]], **kwargs: Any) -> Any:
        ...

