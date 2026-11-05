"""
Optional LLM Provider Adapters for DIL.

========================================================================================
WHY THIS MODULE EXISTS & DIL'S MODEL-AGNOSTIC ARCHITECTURE:
----------------------------------------------------------------------------------------
1. DIL NEVER REQUIRES OPENAI OR ANY SPECIFIC LLM.
   DIL's core philosophy is: "Code calculates and decides; LLMs explain."
   All terminology matching, parameter extraction, financial calculations (LTV, DTI, DSCR,
   Nayak MPBF), and statutory regulatory compliance checks run locally in 100% pure Python
   in under 4 milliseconds with zero external API calls or token costs.

2. PURE CONVENIENCE ADAPTERS:
   This module provides optional, plug-and-play helper functions for developers who want
   a quick one-liner to connect DIL to their favorite LLM provider:
   - OpenAI (GPT-4o, GPT-4o-mini)
   - Google Gemini (Gemini 1.5 Pro / Flash)
   - Local Ollama / vLLM (Llama 3, Mistral - zero cloud cost, 100% air-gapped)
   - Generic Custom Callables (any Python function or enterprise API)

3. FULL INDEPENDENCE:
   You do NOT have to use these functions. You can simply call:
       result, messages = agent.prepare(question)
   and pass `messages` directly into your existing LangChain, LlamaIndex, vLLM,
   or private bank model pipeline!
========================================================================================
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any, Callable, Dict, List, Optional


def create_openai_callable(
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.2,
    client: Optional[Any] = None,
) -> Callable[..., str]:
    """
    Optional convenience adapter for OpenAI models.
    Requires: pip install openai
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "The 'openai' package is required to use create_openai_callable. "
            "Install it via: pip install openai"
        )

    resolved_client = client or OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def _call(messages: List[Dict[str, str]], **kwargs: Any) -> str:
        merged_kwargs = {
            "model": model,
            "temperature": temperature,
            "messages": messages,
        }
        merged_kwargs.update(kwargs)
        response = resolved_client.chat.completions.create(**merged_kwargs)
        return response.choices[0].message.content

    return _call


def create_gemini_callable(
    api_key: Optional[str] = None,
    model: str = "gemini-1.5-flash",
    temperature: float = 0.2,
) -> Callable[..., str]:
    """
    Optional convenience adapter for Google Gemini models.
    Requires: pip install google-generativeai
    """
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "The 'google-generativeai' package is required to use create_gemini_callable. "
            "Install it via: pip install google-generativeai"
        )

    resolved_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if resolved_key:
        genai.configure(api_key=resolved_key)

    gemini_model = genai.GenerativeModel(
        model_name=model,
        generation_config={"temperature": temperature},
    )

    def _call(messages: List[Dict[str, str]], **kwargs: Any) -> str:
        # Convert standard chat messages into a structured prompt
        system_instruction = "\n".join(m["content"] for m in messages if m["role"] == "system")
        conversation = "\n\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in messages if m["role"] != "system"
        )
        full_prompt = f"{system_instruction}\n\n{conversation}".strip()
        response = gemini_model.generate_content(full_prompt)
        return response.text

    return _call


def create_ollama_callable(
    model: str = "llama3:latest",
    host: str = "http://localhost:11434",
    temperature: float = 0.2,
) -> Callable[..., str]:
    """
    Optional zero-cost, local offline adapter for Ollama.
    Requires a running local Ollama instance (http://localhost:11434).
    Zero cloud dependencies, zero data leakage, ideal for air-gapped bank deployments.
    """
    def _call(messages: List[Dict[str, str]], **kwargs: Any) -> str:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        req = urllib.request.Request(
            f"{host}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["message"]["content"]

    return _call


def create_generic_callable(
    fn: Callable[[List[Dict[str, str]]], str]
) -> Callable[..., str]:
    """
    Wraps any arbitrary user-defined callable or private enterprise LLM endpoint.
    Example:
        def my_bank_internal_llm(messages):
            return call_internal_service(messages)

        llm = create_generic_callable(my_bank_internal_llm)
    """
    return fn
