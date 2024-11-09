from pathlib import Path

from datasus_metadata import update_files


if __name__ == "__main__":
    update_files(Path("metadata/files"))
