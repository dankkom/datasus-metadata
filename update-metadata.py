from pathlib import Path

from datasus_metadata import update_aux, update_docs, update_data_files, update_index

if __name__ == "__main__":
    update_data_files(Path("metadata/data"))
    update_docs(Path("metadata/documentation"))
    update_aux(Path("metadata/auxiliary"))
    update_index(Path("metadata"))
