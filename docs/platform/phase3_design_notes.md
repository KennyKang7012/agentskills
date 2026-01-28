# Phase 3 平臺化設計 (概念說明)

本文件概述了系統從靜態整合轉向動態、技能無關 (skill-agnostic) 平臺的架構轉型。

## 1. 前端 UI 動態生成
為了支援多種技能而無需手動更新 UI，我們將實作「Manifest-to-UI」模式。

### 後端元數據 API
- **新路由**: `/api/skills/{skill_id}/manifest`
- **角色**: 回傳該技能在 `SKILL.md` 中定義的輸入需求。

### 前端動態渲染
- **掃描與列表**: UI 獲取所有可用技能並顯示在下拉選單中。
- **動態表單**: 選擇技能後，JS 函數會清空上傳區域，並根據 Manifest 生成新的輸入項。
- **驗證**: 檔案副檔名檢查將根據 Manifest 的 `accept` 欄位動態執行。

## 2. 多格式支援 (PDF/舊版格式)
對於 PDF 等未來格式，系統將支援兩種擴充路徑：

- **路徑 A：技能專業化**: 建立專門的技能 `pdf-report-improvement`，擁有其專屬的依賴項（如 `PyMuPDF`）。
- **路徑 B：通用轉換器**: 實作一個共享的「預處理層」，在發送給 LLM 之前，將各種格式（PDF、PPT、DOCX）轉換為統一的中間格式（如結構化的 Text/JSON）。

## 3. 技能生命週期管理
為了管理日益增多的技能：

| 階段 | 動作 |
| :--- | :--- |
| **自動發現 (Discovery)** | 系統啟動時掃描 `.agent/skills/` 中包含 `SKILL.md` 的資料夾。 |
| **自動配置 (Provisioning)** | 為新技能自動建立本地 `venv` 並執行 `pip install -r requirements.txt`。 |
| **執行 (Execution)** | 標準化的 `SkillRunner` 負責處理 subprocess 呼叫、結束代碼與日誌擷取。 |
| **遠測與診斷 (Telemetry)** | 將所有技能的日誌集中存儲於 `uploads/logs/` 目錄，以便除錯。 |

> [!NOTE]
> 本計劃的核心在於 **「解耦 (Decoupling)」**。核心網頁應用程式應充當處理身份驗證、路由和 UI 佈局的「外殼 (Shell)」，而所有業務邏輯應嚴格保留在技能包中。
