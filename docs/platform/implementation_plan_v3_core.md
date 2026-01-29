# 實作計畫：動態技能平臺化核心 (Phase 3 Core)

將靜態的 `SkillManager` 重構為一個能自動掃描與解析技能包的動態註冊表 (Registry)。

## 預計改動內容

### 後端：技能管理服務 (Skill Management Service)

#### [修改] [skill_manager.py](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/app/services/skill_manager.py)
- **新增 `Skill` 類別**：封裝個別技能的元數據、路徑與執行邏輯。
- **`SkillRegistry` 邏輯**：
    - 實作 `scan_skills()`：自動偵測 `.agent/skills` 下的子目錄。
    - 實作 `load_manifest(skill_path)`：結合 **智慧回退 (Smart Fallback)** 邏輯（正則表達式 + 手動分割）來解析 `SKILL.md`。
    - 維護一個 `Skill` 物件的字典以供查詢。
- **標準化執行**：更新 `run_improvement`（或建立通用的 `execute_skill`）來處理跨平臺的 `venv` 路徑。

### 後端：API 層 (API Layer)

#### [修改] [upload.py](file:///Users/kennykang/Desktop/VibeProj/Anti/agentskills/app/api/upload.py)
- **新增 GET `/api/skills`**：回傳已發現的技能列表（包含名稱與描述）。
- **新增 GET `/api/skills/{skill_id}/manifest`**：回傳特定技能的完整元數據。

## 驗證計畫

### 自動化測試
- 建立 `tests/test_skill_registry.py` 以驗證：
    - 掃描功能是否能正確偵測到 `fa-report-improvement`。
    - Manifest 解析是否能正確處理 YAML 並在必要時成功回退。
    - `os.path` 的處理是否具備平台一致性。

### 手動驗證
- 使用 `curl` 或瀏覽器驗證新的 API 端點。
- 確保現有的 FA 報告優化流程在 `SkillManager` 內仍能正常運作。
