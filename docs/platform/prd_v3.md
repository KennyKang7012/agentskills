# 軟體開發需求文件 (PRD) - Phase 3 平臺化升級

## 1. 目標
將系統從單一用途的 FA 報告優化工具，升級為通用的 **Agent Skills 執行平臺**。支援動態技能發現、元數據驅動的 UI 生成以及多環境隔離執行。

## 2. 核心功能需求

### 2.1 技能動態發現 (Dynamic Skill Discovery)
- 系統啟動時自動掃描 `.agent/skills/` 目錄。
- 解析每個技能包中的 `SKILL.md` (YAML Frontmatter)。
- 建立全域技能註冊表 (Skill Registry)。

### 2.2 元數據驅動 UI (Metadata-Driven UI)
- 前端不再使用硬編碼的 HTML 欄位。
- 透過 API 獲取技能的 `manifest`，動態生成檔案上傳區塊與參數輸入框。
- 支援副檔名預校驗 (基於 Manifest 定義)。

### 2.3 執行隔離與標準化 (Standardized Execution)
- 每個技能擁有獨立的 `venv`。
- 統一透過 `SkillRunner` 調用，標準化參數傳遞與日誌捕捉。
- 支援非同步任務處理與狀態回傳。

## 3. 成功指標
- 新增一個技能包只需放入目錄，無需修改任何後端 API 程式碼。
- 前端能自動顯示新技能的輸入界面。
