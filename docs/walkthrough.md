# 測試與驗證指南 (Walkthrough)

本指南將引導您如何測試與驗證新開發的 FA 報告優化系統。

## 1. 準備工作與啟動伺服器

### 步驟 1：配置環境變數
請確保您已建立 `.env` 檔案。若要使用 **Ollama (本地模型)**，請參考 `.env.example` 中的註釋進行設定：
```properties
# Ollama 範例
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL=llama3.1:latest
```

### 步驟 2：執行啟動指令
請確保您在專案根目錄下，使用 `uv` 啟動服務：

```powershell
# 確保依賴已同步
uv sync

# 啟動應用程式 (Port 8001)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

伺服器啟動後，請開啟瀏覽器並訪問：
[http://localhost:8001](http://localhost:8001)

## 2. 驗證步驟
## 2. UI 測試步驟

### 步驟 A：前端介面測試
1. **載入驗證**: 確認網頁是否正確顯示「FA Report Improvement」標題，且具備現代化的雙區域上傳設計。
2. **樣式檢查**: 確認是否有深色背景、紫色漸層標題以及整齊的卡片佈局。

### 模式 A：標準優化模式 (不含提示詞)
1. 在網頁左側上傳 `.pptx` 報告。
2. 在網頁右側上傳 `.json` 評核檔。
3. **保持提示詞輸入框為空。**
4. 點擊「開始優化報告」。
5. **預期結果**：系統直接呼叫技能包，產出優化報告。

### 模式 B：AI 加工優化模式 (含提示詞)
1. 同樣上傳 `.pptx` 與 `.json`。
2. 在「優化提示詞」輸入框填入具體要求，例如：
   - "請特別加強根因分析部分的數據豐富度。"
   - "調整改善對策，建議加入製程自動化監修。"
3. 點擊「開始優化報告」。
4. **預期結果**：
   - 後端會顯示 `啟動 AI 加工模式`。
   - LLM 會先修飾 JSON 內容，最後才執行優化。

## 3. API 驗證 (使用 curl)

若要直接測試整合提示詞的載入點：

```bash
curl -X POST http://localhost:8001/api/upload \
  -F "report=@your_report.pptx" \
  -F "evaluation_json=@your_eval.json" \
  -F "prompt=請加強統計分析部分的專業性"
```

## 4. 下載功能驗證
1. 待優化完成後，點擊頁面上的「下載優化後的報告」按鈕。
2. **檔名檢查**: 確認下載的檔案名稱格式為 `[原始檔名]_improved_[時間戳].pptx` (例如 `Report_improved_20240128_123055.pptx`)。

## 3. 預期結果
- 後端終端機應顯示處理進度。
- `uploads/` 資料夾中應出現原始上傳檔案與處理後的輸出檔案。
- 前端應提供正確的下載連結。

## 4. 常見問題排除
- **連接拒絕**: 檢查 8001 端口是否被佔用。
- **模組錯誤**: 確保已執行 `export PYTHONPATH=.`。

---

# 實作記錄：API 安全強化與高效對接 (v2.1.6)

本階段成功實作了 API Key 驗證機制，並新增了「一步到位」的高效對接接口，全面提升系統的安全與整合性。

## 完成的功能

### 1. 安全驗證體系 (v2.1.5)
- **智慧識別依賴 (get_api_key)**：
    - **內部請求**：自動識別來自 Web UI 的瀏覽器請求，保持免金鑰的直覺操作。
    - **外部請求**：強制校驗 `X-API-Key` 標頭，保護 `POST /api/upload`、`POST /api/upload-direct` 與 `GET /api/download`。
- **配置管理**：支援 `.env` 驅動，預設金鑰為 `agent-skills-secret-2026`。

### 2. 「一步到位」直接下載接口 (v2.1.6)
- **接口路由**：`POST /api/upload-direct`
- **功能簡介**：調用端僅需一次請求即可同步完成上傳、AI 優化並直接獲取 `.pptx` 檔案串流，大幅簡化外部伺服器的對接開發難度。

## 驗證結果與排錯指南

我們透過真實的 FA 報告（約 2MB+）完成了全流程驗證：

| 測試場景 | 方法 | 預期結果 | 測試狀態 | 備註 |
| :--- | :--- | :--- | :--- | :--- |
| **外部請求 (無金鑰)** | CLI | 403 Forbidden | ✅ 成功攔截 | 有效防止未授權存取 |
| **外部請求 (正確金鑰)** | CLI | 200 OK | ✅ 驗證通過 | 順利進入處理流程 |
| **一步到位下載** | CLI | 直接存為檔案 | ✅ 驗證通過 | 成功產出 2MB+ 報告 |
| **Web UI 操作** | 瀏覽器 | 正常使用 | ✅ 無感相容 | 使用者體驗不受影響 |

## 技術心得與開發筆記

在測試過程中，我們獲得了對接真實大檔案的關鍵經驗：

- **效能預期**：處理真實 PPT 檔案包含 AI 運算，平均耗時為 **15-30 秒**。初次對接時若使用 Dummy 資料會產生「極快」的錯覺，對接生產環境時必須將 **Timeout 設為 60-90 秒**。
- **日誌追蹤**：已在後端增加 `Starting processing...` 與 `Processing finished...` 日誌，能有效排除開發時的「卡頓感」或是程序中斷疑慮。
- **Content-Type 穩定性**：明確指定 `media_type` 為 PowerPoint 格式，確保調用端（如 Python httpx 或 curl）能精確識別回傳內容。

## 修改過的檔案
- [app/api/upload.py](file:///d:/VibeCoding/agentskills/app/api/upload.py) (核心邏輯與安全性)
- [.env](file:///d:/VibeCoding/agentskills/.env) (金鑰配置)
- [docs/api_integration_guide.md](file:///d:/VibeCoding/agentskills/docs/api_integration_guide.md) (技術文件)
- [docs/task.md](file:///d:/VibeCoding/agentskills/docs/task.md) (進度更新)
- [docs/prd.md](file:///d:/VibeCoding/agentskills/docs/prd.md) (版本歷史)

## 📁 最終狀態
- **PRD**: 已更新版本歷史與健壯性詳解。
- **README**: 強調了 v2.1.3 新增的韌性功能。
- **技能文件**: 已將所有指南的版本號統一。
- **Git**: 所有變更已提交並同步。

*專案狀態：已完成並通過驗證 (v2.1.3)* 🚀
