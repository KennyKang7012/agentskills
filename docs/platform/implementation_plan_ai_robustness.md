# 實作計畫：AI JSON 解析強健化 (Robust AI Parsing)

解決使用者回報的「Extra data」錯誤，該錯誤是由於 LLM 在回傳 JSON 的同時附帶了額外的文字說明所引起的。

## 預計改動內容

### 服務層：LLM 客戶端

#### [修改] [llm_client.py](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/app/services/llm_client.py)
- **重構解析邏輯**：不再只是簡單的 `replace` 和 `strip`，改用智慧型擷取方式。
- **實作 JSON 擷取**：
    - 尋找字串中第一個 `{` 和最後一個 `}`。
    - 擷取該區間的子字串作為真正的 JSON 內容。
    - 增加更詳細的錯誤日誌紀錄，包含原始回傳內容的前 100 個字，方便除錯。

## 驗證計畫

### 自動化測試 (腳本驗證)
建立並執行 [tests/test_llm_parsing.py](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/tests/test_llm_parsing.py)：
- 測試案例 1：標準 JSON（正常通過）。
- 測試案例 2：帶有 Markdown 區塊的 JSON（正常通過）。
- 測試案例 3：JSON 前後帶有廢話文字（如 "這是修改後的結果：{...} 希望對你有幫助"）（**核心修復目標**）。

### 手動驗證
- 在系統中重複使用者剛才的步驟，輸入提示詞並執行。
- 檢查 `/api/upload` 是否不再出現「Extra data」錯誤，且順利完成 AI 加工。
