from pathlib import Path
import yaml
from contextforge.models import Project
from contextforge.config import get_config_dir

def save_projects(projects: list[Project], org: str, base_dir: Path | None = None) -> None:
    root = get_config_dir(base_dir)
    store_dir = root / org
    store_file = store_dir / "projects.yaml"
    store_dir.mkdir(parents=True, exist_ok=True)
    with open(store_file, "w") as f:
        yaml.dump([p.model_dump() for p in projects], f)

def load_projects(org: str, base_dir: Path | None = None) -> list[Project]:
    root = get_config_dir(base_dir)
    store_file = root / org / "projects.yaml"
    if store_file.exists():
        with open(store_file, "r") as f:
            data = yaml.safe_load(f)
            return [Project(**p) for p in data]
    return []
