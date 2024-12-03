import shutil
from pathlib import Path


if __name__ == "__main__":
    metadata_dir = Path("metadata")
    data_dir = Path("data")
    for file in metadata_dir.glob("**/*.json"):
        dest_filename = file.name.replace("-", "_")
        dest_filepath = data_dir / file.relative_to(metadata_dir)
        dest_filepath = dest_filepath.with_name(dest_filename)
        dest_filepath.parent.mkdir(parents=True, exist_ok=True)
        print(f"Copying {file} to {dest_filepath}")
        shutil.copy(file, dest_filepath)
