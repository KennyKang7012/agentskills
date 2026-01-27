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

## 4. 驗證計畫
- [ ] **單元測試**: 測試技能元數據解析是否正確。
- [ ] **整合測試**: 上傳一個樣本 `.pptx` 檔案，確保系統能呼叫 LLM 並產生優化後的報告。
- [ ] **UI 測試**: 確保前端在不同瀏覽器下的顯示與互動正常。

## 使用者評論請求
> [!IMPORTANT]
> 1. 請確認 `gpt-oss-20b` 的 API 金鑰與 Endpoint 已就緒。
> 2. 是否需要額外支援 LibreOffice 在環境中的路徑配置？
