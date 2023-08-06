from pathlib import Path

ROOT_DIR = Path(__file__).parent

STATE_FILE: Path = ROOT_DIR / ".hackgame_cli_state"
PLAYER_TOKEN_FILE: Path = ROOT_DIR / ".player_token"
GAME_TOKEN_FILE: Path = ROOT_DIR / ".game_token"
