# 軟體需求文件 (PRD) - FA 報告執行回報與封閉循環驗證

## 1. 專案目標
在 FA 報告優化完成後，由 Python 腳本產生一份結構化的「執行回報」(Success Manifest)，列出實際對 PPTX 進行的修改。這份回報將作為後續 LLM 進行「最終總結」與「品質核對」的依據，解決 LLM 無法直接有效讀取 PPTX 檔案的痛點。

## 2. 規格需求
- **R1: 執行追蹤**：腳本在執行過程中，必須記錄每一個被添加的投影片維度（維度名稱、投影片位置、注入的建議數量）。
- **R2: 輸出格式 (JSON)**：產出一份 `[output_name]_manifest.json`，包含：
    - `timestamp`: 執行時間
    - `input_file`: 原始檔案
    - `output_file`: 產出檔案
    - `items_added`: 已添加的改善項目列表
    - `summary_content`: 注入到總結頁的關鍵文字摘要
- **R3: 錯誤處理記錄**：若某個維度因數據缺失而跳過，必須記錄在 manifest 的 `skipped_items` 中。

## 3. 欄位定義示例
```json
{
  "execution_status": "success",
  "added_slides": [
    {"dimension": "基本資訊完整性", "index": 2, "suggestions_count": 2},
    {"dimension": "根因分析", "index": 8, "suggestions_count": 3}
  ],
  "summary_applied": true,
  "warnings": []
}
```

## 4. 驗證情境
- 當執行完改善腳本，目錄下應多出一個對應的 `_manifest.json` 檔案。
- 檔案內容應準確反映腳本在終端機輸出的「✓ 或 ✗」狀態。
