import subprocess
import os

import platform
import sys

class SkillManager:
    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.script_path = os.path.join(skill_path, "scripts", "improve_fa_report.py")
        self.python_executable = self._get_python_executable()

    def _get_python_executable(self):
        """偵測並返回虛擬環境中的 Python 執行檔路徑"""
        if platform.system() == "Windows":
            venv_python = os.path.join(self.skill_path, "venv", "Scripts", "python.exe")
        else:
            venv_python = os.path.join(self.skill_path, "venv", "bin", "python")
            
        if os.path.exists(venv_python):
            print(f"Using virtual environment python: {venv_python}")
            return venv_python
        
        print(f"Warning: Virtual environment not found at {venv_python}. Using system python.")
        return sys.executable

    def run_improvement(self, input_file: str, eval_json: str, output_file: str):
        # 這裡會執行技能包中的 Python 腳本
        try:
            print(f"Executing script: {self.script_path}")
            result = subprocess.run(
                [self.python_executable, self.script_path, input_file, eval_json, output_file],
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Script execution failed.\nStdout: {e.stdout}\nStderr: {e.stderr}"
            print(error_msg)
            return False, error_msg

# 初始化技能管理器，優先從環境變數讀取路徑
# 預設為相對於 app 目錄的 agentskills 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
# 假設專案結構為 root/app/services，skill 在 root/.agent/skills/fa-report-improvement
DEFAULT_SKILL_PATH = os.path.abspath(os.path.join(current_dir, "../../.agent/skills/fa-report-improvement"))
skill_path = os.getenv("SKILL_PATH", DEFAULT_SKILL_PATH)

skill_manager = SkillManager(skill_path)
