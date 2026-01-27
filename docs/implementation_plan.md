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
- [ ] **提示詞功能開發**: 
    - 修改 `index.html` 加入 Prompt TextArea。
    - 修改 `/api/upload` 接收 `prompt` 字串參數。
- [ ] **LLM 二次加工模組**:
    - 在 `llm_client.py` 中實作 `refine_evaluation_json` 方法。
    - 模型接收「原始 JSON + Prompt」後輸出「優化後的 JSON」。
- [ ] **整合執行鏈路**:
    - 實作條件邏輯：`if prompt: refine_json_via_llm() else: use_original_json()`。
    - 最後統一將結果餵給 `SkillManager` 執行。

## 5. 驗證計畫
- [ ] **自動化測試**: 僅上傳一個 PPT 樣本，驗證是否能產出正確格式的 `improved_*.pptx`。
- [ ] **AI 評分品質檢查**: 確認 LLM 產生的 JSON 評分是否符合邏輯。
