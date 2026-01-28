import httpx
import os
from typing import List, Dict

class LLMClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "your-api-key")
        self.base_url = base_url or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.model = os.getenv("OPENAI_MODEL", "gpt-oss-20b")

    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7
                },
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def refine_evaluation_json(self, original_json: dict, user_prompt: str):
        """根據使用者提示詞優化評核 JSON"""
        system_prompt = (
            "你是一位半導體失效分析 (FA) 專家。使用者會提供一份 8D 評核 JSON 與一段指示。\n"
            "請根據指示修改該 JSON 中的 'total_score', 'dimensions' 或是相關具體建議內容。\n"
            "你必須僅輸出修改後的完整 JSON 字串，不要包含任何開場白或解釋性文字。"
        )
        
        user_content = (
            f"原始 JSON 內容：\n{json.dumps(original_json, ensure_ascii=False)}\n\n"
            f"使用者優化指示：\n{user_prompt}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        try:
            import json
            raw_response = await self.chat_completion(messages)
            # 嘗試解析回傳內容，去除可能的 markdown 區塊標註
            json_str = raw_response.strip().replace("```json", "").replace("```", "").strip()
            refined_data = json.loads(json_str)
            return True, refined_data
        except Exception as e:
            return False, str(e)

llm_client = LLMClient()
