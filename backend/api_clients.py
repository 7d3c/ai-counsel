"""Direct API clients for multiple LLM providers."""

import httpx
from typing import List, Dict, Any, Optional
from .config import (
    ANTHROPIC_API_KEY,
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
    XAI_API_KEY
)


class APIClient:
    """Base class for API clients."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def query(
        self,
        messages: List[Dict[str, str]],
        timeout: float = 120.0
    ) -> Optional[Dict[str, Any]]:
        """Query the API and return standardized response."""
        raise NotImplementedError


class ClaudeClient(APIClient):
    """Anthropic Claude API client."""

    API_URL = "https://api.anthropic.com/v1/messages"

    async def query(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-sonnet-4.5-20250514",
        timeout: float = 120.0
    ) -> Optional[Dict[str, Any]]:
        """Query Claude API."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        payload = {
            "model": model,
            "max_tokens": 4096,
            "messages": messages,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.API_URL,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                data = response.json()
                content = data['content'][0]['text']

                return {
                    'content': content,
                }

        except Exception as e:
            print(f"Error querying Claude API: {e}")
            return None


class GeminiClient(APIClient):
    """Google Gemini API client."""

    API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    async def query(
        self,
        messages: List[Dict[str, str]],
        model: str = "gemini-2.0-flash-exp",
        timeout: float = 120.0
    ) -> Optional[Dict[str, Any]]:
        """Query Gemini API."""
        url = self.API_URL_TEMPLATE.format(model=model)

        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 1.0,
                "maxOutputTokens": 8192,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    params={"key": self.api_key},
                    json=payload
                )
                response.raise_for_status()

                data = response.json()
                content = data['candidates'][0]['content']['parts'][0]['text']

                return {
                    'content': content,
                }

        except Exception as e:
            print(f"Error querying Gemini API: {e}")
            return None


class OpenAIClient(APIClient):
    """OpenAI API client."""

    API_URL = "https://api.openai.com/v1/chat/completions"

    async def query(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        timeout: float = 120.0
    ) -> Optional[Dict[str, Any]]:
        """Query OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": messages,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.API_URL,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                data = response.json()
                content = data['choices'][0]['message']['content']

                return {
                    'content': content,
                }

        except Exception as e:
            print(f"Error querying OpenAI API: {e}")
            return None


class GrokClient(APIClient):
    """xAI Grok API client (OpenAI-compatible)."""

    API_URL = "https://api.x.ai/v1/chat/completions"

    async def query(
        self,
        messages: List[Dict[str, str]],
        model: str = "grok-beta",
        timeout: float = 120.0
    ) -> Optional[Dict[str, Any]]:
        """Query Grok API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": messages,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.API_URL,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                data = response.json()
                content = data['choices'][0]['message']['content']

                return {
                    'content': content,
                }

        except Exception as e:
            print(f"Error querying Grok API: {e}")
            return None


# Model registry - maps model identifiers to (client_class, model_name)
MODEL_REGISTRY = {
    # Claude models
    "claude-sonnet-4.5": (ClaudeClient, "claude-sonnet-4.5-20250514"),
    "claude-sonnet-4": (ClaudeClient, "claude-sonnet-4-20250514"),
    "claude-opus-4": (ClaudeClient, "claude-opus-4-20250514"),

    # Gemini models
    "gemini-2.0-flash": (GeminiClient, "gemini-2.0-flash-exp"),
    "gemini-2.5-flash": (GeminiClient, "gemini-2.5-flash"),
    "gemini-3-pro": (GeminiClient, "gemini-3-pro-preview"),

    # OpenAI models
    "gpt-4o": (OpenAIClient, "gpt-4o"),
    "gpt-4o-mini": (OpenAIClient, "gpt-4o-mini"),
    "gpt-5.1": (OpenAIClient, "gpt-5.1"),
    "o1": (OpenAIClient, "o1"),
    "o1-mini": (OpenAIClient, "o1-mini"),

    # Grok models
    "grok-beta": (GrokClient, "grok-beta"),
    "grok-4": (GrokClient, "grok-4"),
}

# API key mapping
API_KEY_MAP = {
    ClaudeClient: ANTHROPIC_API_KEY,
    GeminiClient: GOOGLE_API_KEY,
    OpenAIClient: OPENAI_API_KEY,
    GrokClient: XAI_API_KEY,
}


async def query_model(
    model_id: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model using the appropriate API client.

    Args:
        model_id: Model identifier from MODEL_REGISTRY
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content', or None if failed
    """
    if model_id not in MODEL_REGISTRY:
        print(f"Unknown model: {model_id}")
        return None

    client_class, model_name = MODEL_REGISTRY[model_id]
    api_key = API_KEY_MAP[client_class]

    if not api_key:
        print(f"No API key configured for {client_class.__name__}")
        return None

    client = client_class(api_key)
    return await client.query(messages, model=model_name, timeout=timeout)


async def query_models_parallel(
    model_ids: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        model_ids: List of model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model_id, messages) for model_id in model_ids]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model_id: response for model_id, response in zip(model_ids, responses)}
