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

## 3. 技能內容的強健性 (Content Robustness)

### 經驗總結 (來自 v2.1.5 修復)
在真實環境（如企業內部）中，輸入的文件格式（如 PPT）往往不符合標準模板。

### 核心原則：容錯處理 (Error Tolerance)
- **非標準佈局處理**：技能在處理文件時，應預期會遇到「缺少標題佔位符」或「非標準版面」。
- **安全獲取機制**：應實作如 `get_or_create_title` 或 `get_or_create_body` 的邏輯，避免因 `AttributeError` 或 `IndexError` 導致整個平臺執行崩潰。
- **降級顯示**：若無法精確修改某個區塊，應採取「新增一頁」而非「強制修改現有頁面」的策略。

## 4. 提交規範 (Commit Policy)
- **原子性提交**：代碼變更、環境配置與對應的文獻改建應合併為同一個 Commit，確保專案歷程的可回溯性。

## 5. Python 開發陷阱與規範 (Technical Pitfalls)

### 延遲匯入錯誤 (Late Import NameError)
- **錯誤案例**：在 `llm_client.py` 中，`json` 模組在函式中段才匯入，但 `json.dumps()` 卻在函式開頭就被呼叫，導致 `NameError`。
- **規範**：所有標準函式庫與第三方套件一律在檔案最頂端匯入。
- **異常防護**：確保所有可能噴出異常的邏輯（特別是處理外部 API 或檔案讀寫）都包覆在完整的 `try...except` 區塊內，並提供精確的日誌輸出。

### LLM 回傳 JSON 擷取 (Extra Data Error)
- **錯誤案例**：LLM 在回傳 JSON 的同時，常會在前後夾雜廢話。若單純使用 `json.loads(content)`，會因為後方的廢話導致 `Extra data` 錯誤。
- **最佳實作**：使用 `json.JSONDecoder().raw_decode(content)` 配合尋找第一個 `{` 的位置。此方法會在解析完第一個完整物件後立刻停止，完美忽略後方的雜訊。
