from pathlib import Path

from datasus_metadados import update


if __name__ == "__main__":
    update(Path("metadados.json"))
