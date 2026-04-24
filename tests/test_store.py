
from contextforge.models import Project
from contextforge.store import load_projects, save_projects


def test_save_and_load_store(tmp_path):
    test_projects = [
        Project(name="project1", repo_url="https://github.com/acme/project1", language="TS", type="app"),
        Project(name="project2", repo_url="https://github.com/acme/project2", language="Python", type="library"),
    ]
    save_projects(test_projects, "TestCorp", base_dir=tmp_path)
    loaded = load_projects("TestCorp", base_dir=tmp_path)
    assert test_projects == loaded