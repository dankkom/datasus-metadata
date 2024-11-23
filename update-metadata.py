from pathlib import Path
from datasus_fetcher.fetcher import connect
from datasus_metadata import update_aux, update_docs, update_data_files, update_index


if __name__ == "__main__":
    metadata_dir = Path("metadata")
    ftp = connect()
    update_data_files(ftp, metadata_dir / "data")
    update_docs(ftp, metadata_dir / "documentation")
    update_aux(ftp, metadata_dir / "auxiliary")
    ftp.close()
    update_index(metadata_dir)
