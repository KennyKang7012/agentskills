# 實作計畫 - 整合 FA 報告優化技能的 FastAPI 應用

本計畫將逐步引導如何建立一個使用 `uv` 管理、FastAPI 驅動並整合 `fa-report-improvement` 技能的網頁應用。

## 1. 準備工作
- [x] 使用 `uv` 初始化專案並建立虛擬環境。
- [x] 安裝必要套件：`fastapi`, `uvicorn`, `python-multipart`, `httpx`, `python-pptx`, `jinja2`。
- [x] 驗證 `gpt-oss-20b` API 連線。

## 2. 後端實作 (FastAPI)
- [x] **建立主程式**: `app/main.py` 處理基本的頁面渲染與 API 路由。
- [x] **技能載入器 (Skill Loader)**:
    - 實作一個類別來讀取 `.agent/skills/fa-report-improvement/SKILL.md`。
    - 封裝執行 `scripts/improve_fa_report.py` 的邏輯。
- [x] **LLM 整合**:
    - 設定 `gpt-oss-20b` 的 API 呼叫邏輯。
- [x] **雙檔案支援**: 實作同時接收 PPT 與 JSON 的 `/api/upload` 路由。

## 3. 前端實作
- [x] **HTML 佈局**: 建立雙檔案上傳區域與狀態顯示頁面。
- [x] **CSS 樣式**: 使用高品質的 Vanilla CSS 設計，包含微動畫與深色模式支援。
- [x] **JavaScript 邏輯**: 實作雙檔案驗證與 Fetch API 提交邏輯。

## 4. Phase 2: 雙文件與提示詞實作計畫
- [x] **提示詞功能開發**: 
    - [x] 修改 `index.html` 加入 Prompt TextArea。
    - [x] 修改 `/api/upload` 接收 `prompt` 字串參數。
- [x] **LLM 二次加工模組**:
    - [x] 在 `llm_client.py` 中實作 `refine_evaluation_json` 方法。
    - [x] 模型接收「原始 JSON + Prompt」後輸出「優化後的 JSON」。
- [x] **整合執行鏈路**:
    - [x] 實作條件邏輯：`if prompt: refine_json_via_llm() else: use_original_json()`。
    - [x] 最後統一將結果餵給 `SkillManager` 執行。

## 5. 驗證計畫
- [x] **自動化測試**: 透過 `walkthrough.md` 提供的流程進行手動驗證。
- [x] **AI 評分品質檢查**: 確認 LLM 產生的 JSON 評分邏輯 (已於 Phase 2 驗證)。

## 6. Phase 3: 系統健壯性與錯誤處理 (Robustness Upgrade) - v2.1.3
本階段落實 [PRD 第 3.5 節](file:///d:/VibeCoding/agentskills/docs/prd.md#L40) 所列之健壯性要求。

### 6.1 後端腳本優化 (Script Level)
- [x] **JSON 清洗器 (Sanitizer)**: 在 `improve_fa_report.py` 中實作正則表達式清理邏輯，自動修補結尾點號或多餘逗號。
- [x] **Markdown 脫殼**: 自動移除 LLM 輸出的 Markdown 代碼塊標記。

### 6.2 API 路由與反饋優化 (API Level)
- [x] **錯誤訊息傳遞**: 修改 `SkillManager` 與 `/api/upload`，將腳本執行失敗的具體 `stderr` 內容精確傳回前端。
- [x] **錯誤分類**: 針對 JSON 損壞或 PPT 轉換失敗提供分類提示。

### 6.3 前端界面強化 (UI Level)
- [x] **即時語法預檢**: 在 `index.html` 中實作 JSON 預解析，攔截語法錯誤並顯示具體診斷。
- [x] **診斷訊息展示**: 優化狀態列顯示邏輯，以紅色警示字體呈現錯誤詳情。

## 7. 更新後的驗證計畫
- [x] **非法 JSON 容錯測試**: 上傳格式錯誤的 JSON，驗證腳本是否能自動修正並執行。
- [x] **錯誤反饋測試**: 上傳完全損壞的 JSON，驗證 UI 是否能精確顯示錯誤診斷訊息。
