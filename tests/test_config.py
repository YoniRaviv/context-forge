from contextforge.models import OrgConfig
from contextforge.config import save_config, load_config

def test_save_and_load_config(tmp_path):
    test_config = OrgConfig(provider="github", org_name="TestCorp", default_branch="develop")
    save_config(config=test_config, base_dir=tmp_path)
    loaded = load_config(tmp_path)
    assert test_config == loaded