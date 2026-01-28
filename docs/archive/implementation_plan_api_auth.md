# API Key 驗證機制實作計畫 (Phase 1)

實作基礎的 API Key 驗證，確保外部伺服器（伺服器 A）與本平台的連線安全性。

## 目的
僅允許持有正確 API Key 的請求呼叫優化接口，並在不影響瀏覽器端使用的前提下實作此功能。

## 預計變更

### 1. 環境配置
- **修改**: [.env.example](file:///d:/VibeCoding/agentskills/.env.example)
- **內容**: 增加 `API_KEY` 範例欄位。

### 2. 安全依賴 (Security Dependency)
- **修改**: [app/api/upload.py](file:///d:/VibeCoding/agentskills/app/api/upload.py)
- **實作**: 
    - 使用 FastAPI 的 `HTTPBearer` 或 `APIKeyHeader`。
    - 考量到瀏覽器端目前沒有 Header，我們將允許兩種模式：
        1.  **Session/Referer 驗證** (針對本系統網頁)。
        2.  **API Key 驗證** (針對外部伺服器 A)。
    - *註：目前為了簡化，我們先實作「若有提供 X-API-Key 則進行驗證」的邏輯，或統一要求所有請求都需具備驗證碼。*

### 3. 下載接口保護
- 確保下載連結也具備一定的保護（或僅限處理中的 Task ID 下載）。目前暫以此 API Key 進行整體保護。

## 驗證計畫

### 自動化腳本測試
1.  建立 `tests/test_api_auth.py`。
2.  **成功測試**: 攜帶正確的 `X-API-Key` 呼叫 `/api/upload`。
3.  **失敗測試**: 攜帶錯誤或不攜帶金鑰呼叫伺服器。

### 手動驗證 (前端調整)
1.  若後端改為強制驗證，需同步更新 `index.html` 的 `fetch` 邏輯以帶入對應金鑰（若金鑰是動態產生的）。
2.  *決策建議*: 針對來自同網域的瀏覽器請求，可以選擇跳過金鑰檢查，僅對外部跨域請求強制執行。
