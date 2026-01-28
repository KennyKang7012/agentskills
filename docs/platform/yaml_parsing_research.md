# 技術研究：如何在 Python 中解析 YAML 元數據 (Frontmatter)

在 Phase 3 中，系統需要讀取 `.agent/skills/*/SKILL.md` 的頭部資訊。這通常被稱為 Frontmatter。

## 1. 建議依賴
雖然可以使用正則表達式 (Regex) 手寫解析，但為了穩健性（處理多行字串、嵌套對象等），強烈建議使用 `PyYAML`。

```bash
# 安裝建議
uv add pyyaml
```

## 2. 實作原型 (Prototype)

以下是一個簡單的 Python 函數，示範如何提取並解析 Frontmatter：

```python
import yaml
import re

def parse_skill_metadata(file_path):
    """
    從 Markdown 檔案中提取 Frontmatter 並轉換為 Python 字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正則表達式匹配兩個 --- 之間的內容
        # ^--- 開頭，$--- 結尾，DOTALL 確保匹配換行符
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
        
        if match:
            frontmatter_raw = match.group(1)
            # 使用 PyYAML 解析字串
            metadata = yaml.safe_load(frontmatter_raw)
            return metadata
        else:
            print(f"Warning: No frontmatter found in {file_path}")
            return None
            
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

# 使用範例
# meta = parse_skill_metadata(".agent/skills/fa-report-improvement/SKILL.md")
# print(meta['name']) # 輸出: fa-report-improvement
```

## 3. 整合至 SkillManager 的架構構想

未來 `SkillManager` 可以演進為：

1. **`scan_skills()`**: 遍歷 `.agent/skills/` 下所有子目錄。
2. **`load_manifest(path)`**: 調用上述解析函數。
3. **`register()`**: 將解析結果存入字典，例如 `self.skills = {"fa-report-improvement": {...}}`。

這將是實現「漸進式揭露」的第一步程式碼基礎。
