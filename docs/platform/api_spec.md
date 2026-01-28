# Phase 3 Skill API Specification (Draft)

為了實現平臺化，所有技能報 (Skill Packages) 必須遵守以下通訊協定。

## 1. 技能清單 (Skill Manifest)
每個技能必須在根目錄包含 `SKILL.md`，其 Frontmatter 必須包含：

```yaml
---
name: string          # 技能唯一識別碼 (slug)
version: string       # 語義化版本 (e.g., 1.0.0)
description: string   # 技能描述 (用於 LLM 識別)
entrypoint: string    # 相對於根目錄的執行路徑 (e.g., scripts/main.py)
inputs:               # 定義前端動態生成的欄位
  - id: string        # 參數名稱
    type: "file" | "text"
    label: string     # 顯示標籤
    accept: string    # (僅限 file) 接受的副檔名，如 ".ppt,.pptx"
    priority: number  # 顯示順序
---
```

## 2. 執行協議 (Execution Protocol)
平臺將透過以下方式調用語音：

```bash
[venv_python] [entrypoint] --[input_id_1] [value1] --[input_id_2] [value2] --output [output_path]
```

- **標準輸出 (Stdout)**: 用於返回處理進度。
- **標準錯誤 (Stderr)**: 用於返回錯誤診斷訊息。
## 4. 跨平台相容性規範 (Cross-Platform)
為了確保 macOS 開發與 Windows 執行無縫對接，必須遵守：

- **路徑處理**: 程式碼內一律使用 `os.path.join()` 或 `pathlib`，嚴禁使用硬編碼的 `/` 或 `\`。
- **編碼格式**: 讀寫 `SKILL.md` 與任何輸出檔案時，必須明確指定 `encoding='utf-8'`。
- **虛擬環境定位**: 平臺應根據 `platform.system()` 動態切換 `bin/python` (Unix) 或 `Scripts/python.exe` (Windows)。
- **Shell 執行**: 避免依賴特定的 Shell 命令 (如 `ls`, `rm`)，應使用 Python 內建模組實作檔案操作。
