from pathlib import Path

from datasus_metadata import update


if __name__ == "__main__":
    update(Path("metadata/files"))
