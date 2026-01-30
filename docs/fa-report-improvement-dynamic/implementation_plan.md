# 重構 FA 報告改善技能：導入動態內容

目前的 `fa-report-improvement` 技能在添加投影片時使用了硬編碼（Hardcoded）的文字範本。這導致它無法真正納入 LLM 在 `evaluation_json` 中產生的特定建議。本計畫旨在讓腳本能夠動態處理內容。

## 擬議變更

### [組件] FA 報告改善技能 (scripts/improve_fa_report.py)

#### [修改] [improve_fa_report.py](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/.agent/skills/fa-report-improvement/scripts/improve_fa_report.py)

1.  **重構 `load_evaluation`**:
    - 增強解析邏輯，從 `improvements` 列表和 `dimension_comments` 中提取以維度名稱為鍵（Key）的建議字典。
    - 鍵對應示例：「基本資訊」-> 基本資訊改善建議，「根因」-> 根因分析建議。
2.  **通用化投影片生成函數**:
    - **`add_basic_info_slide`**：不再使用硬編碼數據（例如 Touch IC "AES2.0"），而是從 `eval_data` 提取數據，並附加 JSON 中的特定改善建議。
    - **`add_statistical_analysis_slide`**：將硬編碼的「1.8MHz 噪聲」文字替換為 JSON 中「根因驗證與統計分析」項目的具體建議。
    - **`add_prevention_measures_slide`**：將硬編碼的 SOP 文字替換為 JSON 中「長期預防措施」或「改善對策」項目的具體建議。
    - **`fix_summary_slide`**：使用 JSON 中的 `summary`、`strengths` 和 `improvements` 來動態填寫總結投影片。
3.  **更新 `improve_report` CLI**:
    - 確保將完整的解析後 `eval_data` 傳遞給所有改善函數。

## 驗證計畫

### 自動化測試
我將建立一個測試腳本，針對樣本 JSON 執行修改後的 Python 腳本，並驗證輸出的 PPTX 是否包含預期文字。

1.  **指令**:
    ```bash
    python scripts/improve_fa_report.py uploads/sample_report.pptx uploads/evaluation_refined.json uploads/test_output.pptx
    ```
2.  **驗證**:
    - 使用輔助腳本讀取 `test_output.pptx`，並斷言（Assert）來自 `evaluation_refined.json` 的特定文字（如「1.8MHz 干擾」或其他具體建議）確實存在於新添加的投影片中。

### 手動驗證
1.  使用 PPT 檢視器打開 `test_output.pptx`，視覺確認新添加的投影片內容來自 `evaluation_refined.json`，而非舊有的硬編碼範本。
