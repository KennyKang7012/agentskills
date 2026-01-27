# FA Report Improvement System 🚀

基於 **FastAPI** 與 **Agent Skills** 的半導體失效分析 (FA) 報告自動化優化平台。本系統整合了現有的 `fa-report-improvement` 技能包，並使用 `gpt-oss-20b` 模型作為核心大腦，協助工程師根據 8D 評核標準優化報告內容。

## ✨ 特色功能

- **雙檔案上傳**: 同時接收 PPT 報告與評核 JSON 檔案。
- **自動化優化**: 整合 8D 評核標準，自動補強報告中的關鍵缺失。
- **現代化介面**: 採用 Vanilla CSS 打造的深色美學介面，支援檔案拖放。
- **虛擬環境管理**: 使用 `uv` 進行高效的套件與環境管理。

## 🛠️ 技術棧

- **後端**: FastAPI (Python)
- **環境管理**: `uv`
- **前端**: HTML5 / CSS3 (Vanilla) / JavaScript
- **AI 模型**: `gpt-oss-20b` (OpenAI 兼容 API)

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

### 3. 啟動伺服器

```bash
export PYTHONPATH=$PYTHONPATH:.
uv run app/main.py
```

開啟瀏覽器訪問：[http://localhost:8000](http://localhost:8000)

## 📂 專案結構

- `app/`: 後端核心邏輯 (FastAPI, Services, API)
- `static/`: 前端樣式與靜態資源
- `templates/`: HTML 模板
- `docs/`: 完整的技術文件 (PRD, Implementation Plan, Walkthrough)
- `uploads/`: 上傳與處理後的檔案存儲處

## 📝 技術文件

- [軟體需求文件 (PRD)](docs/prd.md)
- [實作計畫](docs/implementation_plan.md)
- [測試與驗證指南](docs/walkthrough.md)

---
Developed with ❤️ using Agent Skills.
