import subprocess
import os
import platform
import sys
import re
import json
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                # 簡單的 Key-Value 解析回退 (針對跨環境相容性)
                metadata = {}
                for line in frontmatter_raw.split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1)
                        metadata[k.strip()] = v.strip().strip('"').strip("'")
                return metadata
    except Exception as e:
        logger.error(f"Error parsing {file_path}: {e}")
    return None

class Skill:
    def __init__(self, skill_id: str, path: str, metadata: dict):
        self.id = skill_id
        self.path = os.path.abspath(path)
        self.metadata = metadata
        self.name = metadata.get('name', skill_id)
        self.description = metadata.get('description', '')
        self.version = metadata.get('version', '0.0.0')
        self.entrypoint = metadata.get('entrypoint', os.path.join("scripts", "improve_fa_report.py"))
        self.python_executable = self._get_python_executable()

    def _get_python_executable(self):
        """偵測並返回該技能虛擬環境中的 Python 執行檔路徑 (跨平台)"""
        if platform.system() == "Windows":
            venv_python = os.path.join(self.path, "venv", "Scripts", "python.exe")
        else:
            venv_python = os.path.join(self.path, "venv", "bin", "python")
            
        if os.path.exists(venv_python):
            return venv_python
        
        logger.warning(f"Skill venv not found at {venv_python}. Using system python.")
        return sys.executable

    def run(self, *args):
        """執行該技能的主程式"""
        script_full_path = os.path.join(self.path, self.entrypoint)
        try:
            logger.info(f"Executing skill '{self.id}' with: {script_full_path}")
            # 組合成執行指令
            cmd = [self.python_executable, script_full_path] + list(args)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                encoding='utf-8',
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"技能執行失敗 ({self.id})。\n[錯誤詳情]: {e.stderr}"
            logger.error(f"Stdout: {e.stdout}")
            logger.error(f"Stderr: {e.stderr}")
            return False, error_msg

class SkillRegistry:
    def __init__(self, skills_root: str):
        self.skills_root = os.path.abspath(skills_root)
        self.skills = {}
        self.scan_skills()

    def scan_skills(self):
        """掃描目錄並加載所有有效的技能包"""
        if not os.path.exists(self.skills_root):
            logger.error(f"Skills directory not found: {self.skills_root}")
            return

        logger.info(f"Scanning skills in: {self.skills_root}")
        for item in os.listdir(self.skills_root):
            item_path = os.path.join(self.skills_root, item)
            
            if os.path.isdir(item_path):
                skill_file = os.path.join(item_path, "SKILL.md")
                metadata = parse_skill_metadata(skill_file)
                
                if metadata:
                    skill_id = metadata.get('name', item)
                    self.skills[skill_id] = Skill(skill_id, item_path, metadata)
                    logger.info(f"  [+] Loaded Skill: {skill_id} (v{self.skills[skill_id].version})")

    def get_skill(self, skill_id: str) -> Skill:
        return self.skills.get(skill_id)

    def list_skills(self):
        return [
            {"id": s.id, "name": s.name, "description": s.description, "version": s.version}
            for s in self.skills.values()
        ]

# 初始化全域註冊表
current_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SKILLS_ROOT = os.path.abspath(os.path.join(current_dir, "../../.agent/skills"))
skills_root = os.getenv("SKILLS_ROOT", DEFAULT_SKILLS_ROOT)

skill_registry = SkillRegistry(skills_root)

# 為了保持向後相容，我們保留一個簡單的介面來調用之前的特定技能
class LegacySkillManager:
    def run_improvement(self, input_file: str, eval_json: str, output_file: str):
        # 預設調用 fa-report-improvement
        skill = skill_registry.get_skill("fa-report-improvement")
        if not skill:
            return False, "找不到核心技能 'fa-report-improvement'"
        return skill.run(input_file, eval_json, output_file)

skill_manager = LegacySkillManager()
