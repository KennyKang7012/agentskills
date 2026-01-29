import httpx
import os
import json
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
                timeout=300.0
            )
            response.raise_for_status()
            resp_json = response.json()
            
            if "choices" not in resp_json or not resp_json["choices"]:
                raise ValueError(f"LLM 回傳格式錯誤: {resp_json}")
                
            content = resp_json["choices"][0]["message"].get("content", "")
            return content

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
            raw_response = await self.chat_completion(messages)
            content = raw_response.strip() if raw_response else ""
            
            if not content:
                return False, "LLM 回傳內容為空 (Empty Content)"

            # 輔助偵錯日誌
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"DEBUG: AI 原始回傳長度: {len(content)}")
            
            import re
            decoder = json.JSONDecoder()
            all_starts = [m.start() for m in re.finditer('{', content)]
            
            if not all_starts:
                return False, f"回傳內容中找不到 '{{'。前 100 字: {content[:100]}"

            for start_index in all_starts:
                try:
                    refined_data, end_pos = decoder.raw_decode(content[start_index:])
                    return True, refined_data
                except json.JSONDecodeError:
                    continue
            
            return False, f"解析失敗。嘗試點數: {len(all_starts)}。內容片段: {content[:100]}"
                
        except httpx.HTTPStatusError as e:
            return False, f"LLM API 錯誤 (HTTP {e.response.status_code}): {e.response.text[:100]}"
        except Exception as e:
            error_msg = str(e) or type(e).__name__
            return False, f"LLM 處理異常: {error_msg}"

llm_client = LLMClient()
