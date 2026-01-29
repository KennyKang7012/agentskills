import json
import asyncio
from app.services.llm_client import llm_client

async def test_parsing_scenarios():
    print("Testing AI JSON Parsing Robustness...")
    
    scenarios = [
        {
            "name": "Standard JSON",
            "raw": '{"total_score": 85, "dimensions": {}}'
        },
        {
            "name": "Markdown Blocked JSON",
            "raw": '```json\n{"total_score": 90, "dimensions": {}}\n```'
        },
        {
            "name": "Conversational Noise",
            "raw": '好的，我已經幫您優化了。這是結果：\n{"total_score": 100, "dimensions": {"info": "added"}}\n希望這對你有幫助！'
        },
        {
            "name": "Nested Braces in Text (Trapping Test)",
            "raw": 'Note: use {braces} like this: {"score": 95}'
        }
    ]
    
    # 手動模擬 llm_client.chat_completion 的回傳來測試解析邏輯
    # 由於 llm_client 是一個 singleton 且 refine_evaluation_json 調用 chat_completion
    # 我們這裡直接定義一個 mock 解析邏輯來驗證 regex/find 邏輯是否正確
    
    def mock_extract(raw_response):
        content = raw_response.strip()
        decoder = json.JSONDecoder()
        import re
        all_starts = [m.start() for m in re.finditer('{', content)]
        for start_index in all_starts:
            try:
                data, end_pos = decoder.raw_decode(content[start_index:])
                return data
            except:
                continue
        return None

    for s in scenarios:
        data = mock_extract(s['raw'])
        if data:
            print(f"✓ {s['name']}: PASSED (Score: {data.get('total_score', data.get('score'))})")
        else:
            print(f"✗ {s['name']}: FAILED (No JSON found)")

if __name__ == "__main__":
    asyncio.run(test_parsing_scenarios())
