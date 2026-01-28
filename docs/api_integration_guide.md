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

### 2.1 上傳並啟動優化任務
*   **路由**: `POST /api/upload`
*   **Content-Type**: `multipart/form-data`

**請求參數 (Request Body):**
| 參數名稱 | 類型 | 說明 |
| :--- | :--- | :--- |
| `report` | File | 待優化的 FA 報告 (.ppt 或 .pptx) |
| `evaluation_json` | File | 評核標準 JSON 檔案 (.json) |
| `prompt` | String | (選填) 優化指示提示詞 |

**成功響應 (200 OK):**
```json
{
  "status": "completed",
  "output_file": "report_improved_20260128_170000.pptx"
}
```

---

### 2.2 下載優化報告
*   **路徑**: `GET /api/download/{filename}`
*   **說明**: 使用從上傳接口獲得的 `output_file` 名稱來下載檔案。

**響應:**
*   **成功**: 二進制檔案串流 (application/vnd.openxmlformats-officedocument.presentationml.presentation)
*   **失敗**: `{"error": "File not found"}`

---

## 3. 進階建議 (未來擴充)

若任務處理時間過長（例如超過 60 秒），建議改為 **異步回調 (Webhook)** 模式：

1.  **伺服器 A 提供一個回調 URL**：例如 `http://server-a.com/api/callback`。
2.  **上傳請求增加回調參數**：`POST /api/upload?callback_url=...`。
3.  **任務完成後主動推播**：本系統優化完成後，主動發送一個 POST 請求給伺服器 A，通知處理成功並附帶下載連結。

### 安全建議
在生產環境中進行伺服器對伺服器 (S2S) 調用時，建議增加 **API Key 驗證**：
- 在 Header 中加入 `X-API-Key: YOUR_SECRET_KEY`。
- 本系統增加一組 Middleware 來驗證該 Header 內容。

---

## 4. 範例程式碼 (Python Requests)

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
