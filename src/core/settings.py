import configparser
from pathlib import Path


ROOT_DIR = Path(Path("./src"))


def get_config():
    config = configparser.ConfigParser()
    config.read(ROOT_DIR / ".." / "secrets" / "secrets.ini")
    return config
