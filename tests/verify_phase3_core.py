from app.services.skill_manager import skill_registry, skill_manager
import json

def test_registry_scanning():
    print("Testing SkillRegistry scanning...")
    skills = skill_registry.list_skills()
    print(f"Discovered skills: {json.dumps(skills, indent=2, ensure_ascii=False)}")
    
    assert len(skills) > 0, "No skills discovered!"
    assert any(s['id'] == 'fa-report-improvement' for s in skills), "fa-report-improvement not found!"
    print("✓ Registry scanning passed.\n")

def test_skill_manifest_retrieval():
    print("Testing Skill manifest retrieval...")
    skill = skill_registry.get_skill('fa-report-improvement')
    assert skill is not None
    print(f"Manifest for '{skill.id}': {json.dumps(skill.metadata, indent=2, ensure_ascii=False)}")
    assert skill.name == 'fa-report-improvement'
    print("✓ Manifest retrieval passed.\n")

def test_legacy_compatibility():
    print("Testing LegacySkillManager compatibility...")
    # 測試是否能獲取到相容性物件
    assert hasattr(skill_manager, 'run_improvement'), "LegacySkillManager missing run_improvement!"
    print("✓ Legacy compatibility check passed.\n")

if __name__ == "__main__":
    try:
        test_registry_scanning()
        test_skill_manifest_retrieval()
        test_legacy_compatibility()
        print("All internal verification tests passed!")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
