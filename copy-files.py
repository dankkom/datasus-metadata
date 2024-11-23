import shutil
from pathlib import Path


if __name__ == "__main__":
    metadata_dir = Path("metadata")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    for file in metadata_dir.glob("**/*.json"):
        dest_filename = file.name.replace("-", "_")
        dest_filepath = data_dir / file.relative_to(metadata_dir)
        dest_filepath = dest_filepath.with_name(dest_filename)
        shutil.copy(file, dest_filepath)
