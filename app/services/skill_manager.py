import subprocess
import os

class SkillManager:
    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.script_path = os.path.join(skill_path, "scripts/improve_fa_report.py")

    def run_improvement(self, input_file: str, eval_json: str, output_file: str):
        # 這裡會執行技能包中的 Python 腳本
        try:
            result = subprocess.run(
                ["python", self.script_path, input_file, eval_json, output_file],
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

# 初始化指向特定路徑的技能管理器
skill_manager = SkillManager("/Users/kennykang/Desktop/VibeProj/Anti/agentskills/.agent/skills/fa-report-improvement")
