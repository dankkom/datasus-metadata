import ftplib
import json
from pathlib import Path

from datasus_fetcher.fetcher import connect, list_dataset_files, list_files
from datasus_fetcher.meta import auxiliary_tables, datasets, docs


def update_files(metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    ftp = connect()
    for dataset in datasets:
        print("Listing files of", dataset)
        data = []
        for remote_file in list_dataset_files(ftp, dataset):
            data.append(
                {
                    "filename": remote_file.filename,
                    "full_path": remote_file.full_path,
                    "datetime": remote_file.datetime.isoformat(),
                    "extension": remote_file.extension,
                    "size": remote_file.size,
                    "dataset": remote_file.dataset,
                    "partition": {
                        "uf": remote_file.partition.uf,
                        "year": remote_file.partition.year,
                        "month": remote_file.partition.month,
                        "version": remote_file.partition.version,
                    },
                }
            )
        if not data:
            print(f"{dataset}: No files found")
            return
        metadata_file_path = metadata_dir_path / f"{dataset}.json"
        with open(metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, default=str, ensure_ascii=False)


def list_documentation_files(ftp: ftplib.FTP, dataset: str) -> list[dict]:
    ftp_dir = docs[dataset]["dir"]
    ftp.cwd(ftp_dir)
    files = list_files(ftp, directory=ftp_dir)
    return files


def update_docs(metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    ftp = connect()
    for doc in docs:
        print("Listing files of", doc)
        data = []
        for file in list_documentation_files(ftp, doc):
            data.append(
                {
                    "filename": file["filename"],
                    "full_path": file["full_path"],
                    "datetime": file["datetime"].isoformat(),
                    "extension": file["extension"],
                    "size": file["size"],
                    "dataset": doc,
                }
            )
        if not data:
            print(f"{doc}: No files found")
            return
        metadata_file_path = metadata_dir_path / f"{doc}.json"
        with open(metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, default=str, ensure_ascii=False)


def list_auxiliary_tables_files(ftp: ftplib.FTP, dataset: str) -> list[dict]:
    ftp_dir = auxiliary_tables[dataset]["dir"]
    ftp.cwd(ftp_dir)
    files = list_files(ftp, directory=ftp_dir)
    return files


def update_aux(metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    ftp = connect()
    for aux in auxiliary_tables:
        print("Listing files of", aux)
        data = []
        for file in list_auxiliary_tables_files(ftp, aux):
            data.append(
                {
                    "filename": file["filename"],
                    "full_path": file["full_path"],
                    "datetime": file["datetime"].isoformat(),
                    "extension": file["extension"],
                    "size": file["size"],
                    "dataset": aux,
                }
            )
        if not data:
            print(f"{aux}: No files found")
            return
        metadata_file_path = metadata_dir_path / f"{aux}.json"
        with open(metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, default=str, ensure_ascii=False)
