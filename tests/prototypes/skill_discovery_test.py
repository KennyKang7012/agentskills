import os
import re
import json

# 設定技能根目錄 (使用 os.path.join 確保平台相容性)
SKILLS_DIR = os.path.join(".agent", "skills")

def parse_skill_metadata(file_path):
    """提取並解析 SKILL.md 中的 YAML Frontmatter (支援 PyYAML 或簡單 Regex 回退)"""
    if not os.path.exists(file_path):
        return None
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
        if match:
            frontmatter_raw = match.group(1)
            try:
                import yaml
                return yaml.safe_load(frontmatter_raw)
            except ImportError:
                # 簡單的 Key-Value 解析回退 (針對 Prototype)
                metadata = {}
                for line in frontmatter_raw.split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        metadata[k.strip()] = v.strip().strip('"').strip("'")
                return metadata
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return None

class SkillRegistryPrototype:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.skills = {}

    def scan(self):
        """掃描目錄並加載所有有效的技能包"""
        if not os.path.exists(self.base_dir):
            print(f"Directory {self.base_dir} not found.")
            return

        print(f"Scanning directory: {self.base_dir}")
        for item in os.listdir(self.base_dir):
            item_path = os.path.join(self.base_dir, item)
            
            # 必須是資料夾，且包含 SKILL.md
            if os.path.isdir(item_path):
                skill_file = os.path.join(item_path, "SKILL.md")
                metadata = parse_skill_metadata(skill_file)
                
                if metadata and 'name' in metadata:
                    skill_id = metadata['name']
                    self.skills[skill_id] = {
                        "path": os.path.abspath(item_path),
                        "metadata": metadata
                    }
                    print(f"  [+] Found Skill: {skill_id} (v{metadata.get('version', 'unknown')})")

    def get_skill_list(self):
        """用於 API 返回的簡化列表"""
        return [
            {
                "id": sid, 
                "name": info['metadata'].get('name'), 
                "description": info['metadata'].get('description')
            } 
            for sid, info in self.skills.items()
        ]

# --- 測試執行 ---
if __name__ == "__main__":
    # 注意：在專案根目錄執行此腳本
    registry = SkillRegistryPrototype(SKILLS_DIR)
    registry.scan()
    
    print("\nRegistry Summary (JSON Format):")
    print(json.dumps(registry.get_skill_list(), indent=2, ensure_ascii=False))
