# Step C: 動態 UI 渲染邏輯草案 (Dynamic UI Design Draft)

為了實現「一次開發、處處適用」的平臺化目標，前端介面必須具備根據技能元數據 (Metadata) 動態生成的能力。

## 1. 核心流程 (The Workflow)

1. **獲取列表**: 頁面載入時，請求 `/api/skills` 填入技能選擇下拉選單 (Dropdown)。
2. **選中技能**: 當使用者選擇某個技能（如 `fa-report-improvement`）時，前端發送請求至 `/api/skills/{id}/manifest`。
3. **渲染 UI**: 前端迴圈 manifest 中的 `inputs` 陣列，動態建立 HTML 元素。
4. **提交任務**: 點擊按鈕時，自動收集這些動態元素的數值，封裝成 `FormData` 送往通用執行接口。

## 2. 元數據與元件映射 (Component Mapping)

Manifest 中的 `type` 將決定前端生成的元件類型：

| Manifest Type | 前端生成元件 (HTML/JS) | 說明 |
| :--- | :--- | :--- |
| **file** | `UploadBlock` (自定義拖拽區塊) | 包含拖拽、選擇檔案、副檔名校驗功能。 |
| **text** | `textarea` 或 `input[type="text"]` | 提供單行或多行文本輸入。 |
| **select** | `select` | 如果 manifest 定義了 `options`，則產生下拉選單。 |

## 3. 前端實作伪代碼 (Front-end Pseudo-code)

```javascript
/**
 * 根據 Manifest 動態渲染 Input 區域
 */
function renderSkillForm(manifest) {
    const container = document.getElementById('dynamic-form-container');
    container.innerHTML = ''; // 清空舊介面

    manifest.inputs.forEach(input => {
        const wrapper = createFieldWrapper(input.label);
        
        if (input.type === 'file') {
            const uploadZone = createUploadZone(input.id, input.accept);
            wrapper.appendChild(uploadZone);
        } else if (input.type === 'text') {
            const textarea = createTextArea(input.id);
            wrapper.appendChild(textarea);
        }
        
        container.appendChild(wrapper);
    });
}
```

## 4. 關鍵挑戰與解決方案

### A. 檔案校驗 (File Validation)
- **挑戰**: 不同技能接受的檔案不同。
- **解決方案**: `accept` 屬性會直接綁定到 `<input type="file">`，並在 JavaScript `drop` 事件中檢查副檔名白名單。

### B. 動態狀態管理 (Dynamic State)
- **挑戰**: 欄位數量不固定，如何收集數據？
- **解決方案**: 提交時遍歷 `manifest.inputs`，根據 `id` 從 DOM 中取值。
  ```javascript
  const formData = new FormData();
  manifest.inputs.forEach(input => {
      const el = document.getElementById(`input-${input.id}`);
      formData.append(input.id, el.files ? el.files[0] : el.value);
  });
  ```

### C. 視覺反饋 (Visual Feedback)
- 即使是動態生成，仍應保持統一的「玻璃擬態 (Glassmorphism)」或「現代簡約」風格，維持 UI 的整體感。
