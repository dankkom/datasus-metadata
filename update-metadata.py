from pathlib import Path
from datasus_fetcher.fetcher import connect
from datasus_metadata import update_aux, update_docs, update_data_files, update_index

if __name__ == "__main__":
    ftp = connect()
    update_data_files(ftp, Path("metadata/data"))
    update_docs(ftp, Path("metadata/documentation"))
    update_aux(ftp, Path("metadata/auxiliary"))
    ftp.close()
    update_index(Path("metadata"))
