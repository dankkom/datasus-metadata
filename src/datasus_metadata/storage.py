import json
from pathlib import Path


def load_json(filepath: Path) -> list | dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: list | dict, filepath: Path):
    print("Saving JSON:", filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=str, ensure_ascii=False)
