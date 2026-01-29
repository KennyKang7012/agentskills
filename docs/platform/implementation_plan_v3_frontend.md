# 實作計畫：前端動態整合 (Phase 3 Frontend)

將 Web UI 從硬編碼重構為「元數據驅動 (Metadata-driven)」的動態介面。

## 預計改動內容

### 前端：使用者介面 (UI)

#### [修改] [index.html](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/templates/index.html)
- **技能選擇器**：新增一個下拉選單 (`<select>`) 用於切換不同的技能。
- **動態表單容器**：建立一個空的 `div`，用於注入動態生成的輸入欄位。
- **JavaScript 邏輯**：
    - `fetchSkills()`：頁面載入時請求 `/api/skills` 並填充選單。
    - `loadSkillUI(skillId)`：選中技能後請求 `/api/skills/{id}` 並渲染 UI。
    - `handleSubmit()`：修改上傳邏輯，根據 Manifest 動態收集數據並提交。

### 前端：樣式與美學

#### [修改] [index.css](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/static/css/index.css) (若存在) 或在 HTML 中內聯
- 確保動態生成的元件（如拖拽區塊、文本框）符合現有的深色模式與平滑動畫風格。

## 實作細節：動態渲染邏輯

1.  **清空容器**：每次切換技能時清空舊有的表單內容。
2.  **循環生成**：遍歷 Manifest 中的 `inputs` 陣列。
3.  **條件分支**：
    - 若 `type === 'file'`：生成帶有 `drag-and-drop` 支援的檔案上傳元件。
    - 若 `type === 'text'`：生成 `textarea` 提供輸入。
4.  **按鈕綁定**：確保「執行優化」按鈕能正確調用通用執行 API。

## 驗證計畫

### 手動驗證
- 切換至 `fa-report-improvement` 技能，確認生成的 UI 與原本的手寫介面一致。
- 嘗試執行上傳，確認後端能正確接收並處理數據。
- 測試非法操作（如未選擇技能即上傳）的錯誤提示。
