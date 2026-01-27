# 軟體開發需求文件 (PRD) - FA 報告優化網頁應用程式

## 1. 專案概述
本專案旨在開發一個基於 FastAPI 的網頁應用程式，整合現有的 `fa-report-improvement` 技能包。使用者可以透過網頁介面上傳半導體失效分析 (FA) 報告（.ppt 或 .pptx），系統將利用 `gpt-oss-20b` 模型（兼容 OpenAI API）作為核心大腦，根據 8D 評核標準提供改進建議並自動優化報告內容。

## 2. 核心技術棧
- **後端框架**: FastAPI (Python)
- **環境管理**: `uv` (高效的 Python 套件與虛擬環境管理工具)
- **前端技術**: 原生 CSS + JavaScript (Vanilla JS)
- **大語言模型 (LLM)**: `gpt-oss-20b` (透過 OpenAI 兼容 API 呼叫)
- **技能包整合**: `@.agent/skills/fa-report-improvement`

## 3. 功能需求

### 3.1 虛擬環境與套件管理
- 使用 `uv` 初始化專案環境。
- 管理 FastAPI, `python-pptx`, `httpx` (用於呼叫 LLM API) 等相依套件。

### 3.2 技能包整合
- **載入技能**: 系統啟動時需掃描 `.agent/skills/` 資料夾。
- **解析元數據**: 讀取 `SKILL.md` 的 Frontmatter (名稱、描述)。
- **指令執行**: 解析使用者需求，動態呼叫技能包中的 Python 腳本（如 `improve_fa_report.py`）。

### 3.3 網頁介面 (Web UI)
- **雙檔案上傳**: 支援同時上傳 FA 報告 (.ppt/.pptx) 與評核 JSON (.json)。
- **分析工作區**: 顯示上傳後的檔案名稱，並在雙檔案備齊後才允許啟動優化任務。
- **優化編輯**: 展示建議改進的內容，並允許使用者確認後由 LLM 自動更新內容。
- **檔案下載**: 優化完成後提供新的 .pptx 檔案下載路由 `/api/download/{filename}`。

### 3.4 AI 模型整合 (gpt-oss-20b)
- 實作 OpenAI 兼容的客戶端連接 `gpt-oss-20b`。
- 設計 Prompt 範本，結合 FA 報告評核標準與技能指令。

## 4. 系統架構 (草案)
- `app/main.py`: FastAPI 進入點與路由。
- `app/services/skill_manager.py`: 負責發現與啟動技能包。
- `app/services/llm_client.py`: 負責與 `gpt-oss-20b` 通訊。
- `static/`: 存放 CSS 與 JavaScript 檔案。
- `templates/`: 存放 HTML 模板。

## 5. 安全性與限制
- **效能**: 檔案轉換過程可能較耗時，需考量非同步處理 (Backgroud Tasks)。
- **相容性**: 必須確保 `uv` 環境中安裝有 LibreOffice 命令行工具以支援 .ppt 轉換。
- **隔離**: 技能執行應確保在指定的專案路徑下。
