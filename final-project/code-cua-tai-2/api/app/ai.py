from dataclasses import dataclass
import json
import httpx
from .config import get_settings

class AIProviderError(Exception):
    pass

@dataclass
class AIResponse:
    text: str
    generated: bool
    sources: list[str]

class LLMProvider:
    async def complete(self, prompt: str, context: list[str]) -> AIResponse:
        raise NotImplementedError

class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 30):
        self.base_url=base_url.rstrip('/')
        self.api_key=api_key
        self.model=model
        self.timeout=timeout

    async def complete(self, prompt: str, context: list[str]) -> AIResponse:
        system='You are a C++ tutor. Prefer the supplied Knowledge Base context, do not invent IDs or citations, and say when context is insufficient.'
        content=f'Knowledge Base context:\n{chr(10).join(context)}\n\nUser request:\n{prompt}'
        headers={'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        payload={'model':self.model,'temperature':0.2,'messages':[{'role':'system','content':system},{'role':'user','content':content}]}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response=await client.post(f'{self.base_url}/chat/completions',headers=headers,json=payload)
                response.raise_for_status()
                body=response.json()
            choices=body.get('choices') if isinstance(body, dict) else None
            content=choices[0].get('message', {}).get('content') if isinstance(choices, list) and choices else None
            if not isinstance(content, str) or not content:
                raise ValueError('LLM response has an invalid shape')
            return AIResponse(text=content,generated=True,sources=[])
        except (httpx.HTTPError, OSError, json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise AIProviderError('AI provider is unavailable') from exc

def configured_provider() -> LLMProvider | None:
    settings=get_settings()
    base_url=getattr(settings,'llm_base_url',None); api_key=getattr(settings,'llm_api_key',None); model=getattr(settings,'llm_model',None)
    if not base_url or not api_key or not model: return None
    return OpenAICompatibleProvider(base_url,api_key,model,getattr(settings,'llm_timeout',30))
