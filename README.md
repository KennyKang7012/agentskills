# FA Report Improvement System 🚀

基於 **FastAPI** 與 **Agent Skills** 的半導體失效分析 (FA) 報告自動化優化平台。本系統整合了現有的 `fa-report-improvement` 技能包，並使用 `gpt-oss-20b` 模型作為核心大腦，協助工程師根據 8D 評核標準優化報告內容。

## ✨ 特色功能

- **雙檔案優化**: 同時受入 FA 報告與評核 JSON 檔案。
- **AI 加工模式 (提示詞引導)**: 整合 LLM (支援 OpenAI / Ollama)，可輸入指示動態調整評核建議。
- **智慧輸出**: 自動生成 `[原始檔名]_improved_[時間戳].pptx`，版本管理更輕鬆。
- **全自動化技能執行**: 獲取最終 JSON 後自動觸發技能包補強報告缺失。
- **現代化美學介面**: 採用深色模式與平滑動畫，極致的工程師使用體驗。
- **檔案拖拽上傳 (v2.1.4 New)**: 支援直接拖曳 `.ppt/.pptx` 與 `.json` 檔案至感應區，操作更直覺。
- **系統健壯性 (v2.1.3)**: 具備 JSON 語法自動容錯解析與精確錯誤反饋機制。
- **API Key 安全驗證 (v2.1.5)**: 針對外部伺服器對接提供 `X-API-Key` 標頭驗證，保障傳輸安全。
- **一步到位對接 (v2.1.6)**: 新增 `/api/upload-direct` 接口，一條指令同步完成上傳、優化與下載。

## 🛠️ 技術棧

- **後端**: FastAPI (Python)
- **環境管理**: `uv`
- **前端**: HTML5 / CSS3 (Vanilla) / JavaScript
- **AI 模型**: `gpt-oss:20b` (OpenAI 兼容 API)

## 🚀 快速啟動

### 1. 安裝環境與相依套件

確保已安裝 `uv`，然後在根目錄執行：

```bash
uv sync
```

### 2. 設定環境變數

複製範例檔案並填入您的 API 金鑰與路徑設定：

```bash
cp .env.example .env
```

編輯 `.env` 檔案：
- `OPENAI_API_KEY`: 您的 gpt-oss-20b API 金鑰。
- `OPENAI_API_BASE`: API 基礎 URL (例如 `https://api.openai.com/v1`)。
- `SKILL_PATH`: 指向 `fa-report-improvement` 技能包的絕對路徑。
- `API_KEY`: 用於外部 API 驗證的秘密金鑰 (預設: `agent-skills-secret-2026`)。

### 3. 啟動伺服器

```powershell
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

開啟瀏覽器訪問：[http://localhost:8001](http://localhost:8001)

## 📂 專案結構

- `app/`: 後端核心邏輯 (FastAPI, Services, API)
- `static/`: 前端樣式與靜態資源
- `templates/`: HTML 模板
- `docs/`: 完整的技術文件 (PRD, Implementation Plan, Walkthrough)
- `uploads/`: 上傳與處理後的檔案存儲處

## 📝 技術文件
- [API 整合指南](docs/api_integration_guide.md) (外部伺服器對接必看)
- [軟體需求文件 (PRD)](docs/prd.md)
- [技術架構文件](docs/technical_architecture.md)
- [實作計畫](docs/implementation_plan.md)
- [測試與驗證指南](docs/walkthrough.md)
- [👉 操作手冊 (v3.0)](docs/user_manual_v3.md)
- [平臺化：動態技能 Manifest 實作計畫](docs/platform/implementation_plan_v3_core.md)
- [平臺化：AI 解析強健化實作計畫](docs/platform/implementation_plan_ai_robustness.md)
- [平臺開發最佳實作](docs/platform/best_practices.md)

---
Developed with ❤️ using Agent Skills.
