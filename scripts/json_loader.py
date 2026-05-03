import json
from pathlib import Path
from typing import Union

def load_json(path: Union[str, Path]) -> list[dict]:
    _path = Path(path)
    if not _path.is_absolute():
        _path = Path(__file__).resolve().parents[1] / _path
    if not _path.exists():
        raise FileNotFoundError(f"JSON file not found at: {path}")
    with _path.open(encoding="utf-8") as fh:
        return json.load(fh)