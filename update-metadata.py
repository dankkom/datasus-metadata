from pathlib import Path

from datasus_metadata import update_aux, update_docs, update_files

if __name__ == "__main__":
    update_files(Path("metadata/files"))
    update_docs(Path("metadata/documentation"))
    update_aux(Path("metadata/auxiliary"))
