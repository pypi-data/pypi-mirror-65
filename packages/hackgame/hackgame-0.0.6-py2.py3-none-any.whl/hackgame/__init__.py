from pathlib import Path

ROOT_DIR = Path(__file__).parent

STATE_FILE: Path = ROOT_DIR / ".hackgame_cli_state"

from . import cli, api, auth, docs, models
