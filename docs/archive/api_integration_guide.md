# API 整合指南：外部伺服器對接手冊

本文件旨在說明外部伺服器（伺服器 A）如何透過 API 與本「FA 報告優化系統」進行整合。

## 1. 核心流程

伺服器 A 與本系統的互動流程建議如下：

1.  **檔案上傳/任務啟動**：伺服器 A 向本系統發送 `POST /api/upload` 請求。
2.  **同步處理**：本系統會在收到請求後開始優化任務。伺服器 A 需等待 HTTP 響應（Response）。
3.  **獲取結果**：HTTP 響應將回傳處理結果與輸出檔名。
4.  **檔案下載**：伺服器 A 根據檔名透過 `GET /api/download/{filename}` 下載優化後的報告。

---

## 2. 接口細節 (Endpoints)

### 2.1 上傳並啟動優化任務 (傳統模式)
*   **路由**: `POST /api/upload`
*   **說明**: 推薦用於需要獲取檔名以進行版本管理的場景。回傳 JSON 包含 `output_file`。

---

### 2.2 上傳並直接獲取檔案 ("一步到位" 模式)
*   **路由**: `POST /api/upload-direct`
*   **Content-Type**: `multipart/form-data`
*   **說明**: 用於一條指令直接完成優化並下載檔案。

**請求參數:** (與 2.1 相同)

**成功響應 (200 OK):**
*   直接回傳二進制檔案串流 (.pptx)。

**使用 CLI 一步下載範例:**
```powershell
curl.exe -H "X-API-Key: YOUR_KEY" -X POST http://localhost:8001/api/upload-direct -F "report=@report.pptx" -F "evaluation_json=@eval.json" -o "improved_final.pptx"
```

---

### 2.3 下載優化報告 (配合 2.1 使用)
*   **路徑**: `GET /api/download/{filename}`
*   **Method**: `GET`
*   **Header**: `X-API-Key: YOUR_KEY`
*   **說明**: 使用從上傳接口獲得的 `output_file` 名稱來下載檔案。

**響應:**
*   **成功**: 二進制檔案串流 (application/vnd.openxmlformats-officedocument.presentationml.presentation)
*   **失敗**: `{"error": "File not found"}` 或 `403 Forbidden` (金鑰錯誤)

### 2.4 處理效能與逾時 (Performance & Timeout)
**現象**：發送請求後看起來「卡住」沒有反應。
- **原因**：本系統整合了 AI Brain 運算與 PPT 渲染引擎。處理一個真實的 PPT 檔案（2MB+）平均需要 **15-30 秒**。
- **對策**：
    - **調高 Timeout**：使用 `curl` 或程式碼調用時，請將 `timeout` 設定在 **60-90 秒** 以上。
    - **避免中斷**：執行中請勿隨意中斷請求，否則伺服器可能會報出 `KeyboardInterrupt` 錯誤。

---

## 3. 進階建議 (未來擴充)

若任務處理時間過長（例如超過 60 秒），建議改為 **異步回調 (Webhook)** 模式：

1.  **伺服器 A 提供一個回調 URL**：例如 `http://server-a.com/api/callback`。
2.  **上傳請求增加回調參數**：`POST /api/upload?callback_url=...`。
3.  **任務完成後主動推播**：本系統優化完成後，主動發送一個 POST 請求給伺服器 A，通知處理成功並附帶下載連結。

---

## 4. 常見問題排查 (Troubleshooting)

### 4.1 curl: (26) Failed to open/read local data
**原因**：`curl` 找不到本地檔案。
- **檢查點**：
    - 檔案路徑前是否漏掉了 **`@`** 符號？ (正確格式: `-F "report=@filename.pptx"`)
    - 檔名是否包含空格？ (建議將整個參數用引號包起來)
    - 副檔名是否正確？ (例如 `.ppt` 與 `.pptx` 是否混淆)

### 4.2 403 Forbidden
**原因**：API Key 驗證失敗。
- **檢查點**：
    - Header 名稱是否為 `X-API-Key`？
    - 金鑰內容是否與伺服器 `.env` 中的 `API_KEY` 一致？

### 4.3 400 Bad Request (Value Error: Expected UploadFile)
**原因**：參數傳遞格式錯誤。
- **檢查點**：
    - 是否漏掉了 `@` 符號導致 `curl` 將檔案當作純字串傳送？

---

## 5. 安全建議

在生產環境中進行伺服器對伺服器 (S2S) 調用時，建議增加 **API Key 驗證**：
- 在 Header 中加入 `X-API-Key: YOUR_SECRET_KEY`。
- 本系統增加一組 Middleware 來驗證該 Header 內容。

---

## 6. 範例程式碼 (Python Requests)

```python
import requests

# 設定參數
url = "http://YOUR_SERVER_IP:8001/api/upload"
files = {
    'report': open('my_report.pptx', 'rb'),
    'evaluation_json': open('eval.json', 'rb')
}
data = {'prompt': '加強根因分析的統計數據'}

# 發送請求 (同步等待)
response = requests.post(url, files=files, data=data)
result = response.json()

if result['status'] == 'completed':
    output_filename = result['output_file']
    # 下載檔案
    download_url = f"http://YOUR_SERVER_IP:8001/api/download/{output_filename}"
    pptx_content = requests.get(download_url).content
    with open("improved_report.pptx", "wb") as f:
        f.write(pptx_content)
    print("優化完成並已下載！")
```

---

## 7. 給 AI 開發助手 (如 Claude Code) 的對接建議

若您使用 Claude Code、GitHub Copilot 或其他 AI 助理來開發對接程式碼，建議直接將本檔案的內容貼給它，並配合以下指令 (Prompt)：

> 「我是開發者，現在要實作一個客戶端來呼叫 **FA Report 改善平台**。請參考 `docs/api_integration_guide.md`，幫我寫一個 Python 腳本，能夠讀取本地的 `.pptx` 與 `.json`，並透過 `/api/upload-direct` 接口獲取優化後的結果並存檔。請注意處理效能延遲，加入適當的 Timeout 設定並顯示進度日誌。」

這樣 AI 助手能根據本指南，精確地實作金鑰驗證與逾時處理邏輯。
