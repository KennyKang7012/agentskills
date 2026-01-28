# 平臺開發最佳實踐 (Best Practices)

本文件記載了在開發 Agent Skills 平臺時採用的工程原則與設計心法。

## 1. 智慧回退機制 (Smart Fallback)

### 設計背景
在 Phase 3 的技能發現 (Skill Discovery) 過程中，系統需要解析 `SKILL.md` 的 YAML 元數據。然而，在某些情況下（如剛部署、虛擬環境未就緒），外部解析庫（如 `PyYAML`）可能尚未安裝。

### 核心原則：防禦性程式設計 (Defensive Programming)
**「核心骨架（內核）應該儘可能減少外部依賴，確保系統始終可掃描、可啟動。」**

### 實作範例
在 `SkillManager` 中，我們採用以下邏輯：
1. **優先使用專業庫**：如果 `PyYAML` 存在，則使用 `yaml.safe_load()` 處理複雜結構。
2. **智慧回退 (Fallback)**：如果找不到庫，則切換至簡單的正則表達式 (Regex) 與字串分割邏輯，抓取基礎的 `name` 與 `description`。

這部分在 `skill_discovery_test.py` 中的核心代碼如下：
```python
if match:
    frontmatter_raw = match.group(1)
    try:
        import yaml  # 嘗試使用專業的 YAML 庫
        return yaml.safe_load(frontmatter_raw)
    except ImportError:
        # --- 智慧回退邏輯 (Fallback) ---
        # 如果環境中沒有安裝 PyYAML，我們手動模擬一個簡單的解析器
        metadata = {}
        for line in frontmatter_raw.split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                # 去掉空白與引號，將 "name: value" 轉存入 dict
                metadata[k.strip()] = v.strip().strip('"').strip("'")
        return metadata
```

### 帶來的價值
- **環境健壯性**：即使環境配置不完全，主平臺介面依然能正常顯示技能列表，並能優雅地提示使用者「需要安裝依賴」。
- **低摩擦啟動**：減少了開發者在不同作業系統（macOS/Windows）間切換時的配置負載。

## 2. 跨平台相容性 (Cross-Platform)

### 工程規範
- **路徑正則化**：一律使用 `os.path.join()`，避免 `/` 或 `\` 的硬編碼問題。
- **編碼一致性**：讀寫檔案必須明確宣告 `encoding='utf-8'`，防止 Windows 環境因 `cp950` 導致的崩潰。
- **環境差異封裝**：將不同系統的 venv 路徑差異（`bin/` vs `Scripts/`）封裝在管理類別內部。
