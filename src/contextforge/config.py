from pathlib import Path
import yaml
from contextforge.models import OrgConfig

CONFIG_DIR = Path.home() / ".contextforge"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

def get_config_dir(base_dir: Path | None = None) -> Path:
    return base_dir / ".contextforge" if base_dir else Path.home() / ".contextforge"

def save_config(config: OrgConfig, base_dir: Path | None = None) -> None:
    config_dir = get_config_dir(base_dir)
    config_file = config_dir / "config.yaml"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        yaml.dump(config.model_dump(), f)

def load_config(base_dir: Path | None = None) -> OrgConfig | None:
    config_dir = get_config_dir(base_dir)
    config_file = config_dir / "config.yaml"
    if config_file.exists():
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
            return OrgConfig(**config)
    else:
        return None
