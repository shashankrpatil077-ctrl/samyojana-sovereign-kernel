import asyncio
import httpx
import re
from typing import Dict, Any

class CascadingInferenceEngine:
    def __init__(self):
        self.vllm_client = httpx.AsyncClient()

    async def route_request(self, user_transcript: str) -> Dict[str, Any]:
        if re.search(r"\b(balance|balanc|bakaya)\b", user_transcript, re.IGNORECASE):
            return {"intent": "BALANCE_INQUIRY", "tier": 1, "confidence": 0.99}

        tier2_result = await self._infer_vllm("Qwen2.5-3B-Instruct", user_transcript, 64)
        if tier2_result["confidence"] > 0.88:
            return {"tier": 2, **tier2_result}

        tier3_result = await self._infer_vllm("Meta-Llama-3.2-8B-Instruct", user_transcript, 256)
        return {"tier": 3, **tier3_result}

    async def _infer_vllm(self, model: str, prompt: str, max_tokens: int) -> Dict[str, Any]:
        payload = {"model": model, "prompt": prompt, "max_tokens": max_tokens, "temperature": 0.0}
        resp = await self.vllm_client.post("http://127.0.0.1:8000/v1/completions", json=payload)
        return resp.json()
