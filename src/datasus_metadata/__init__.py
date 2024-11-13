import ftplib
import json
from pathlib import Path

from datasus_fetcher.fetcher import list_dataset_files, list_files
from datasus_fetcher.meta import auxiliary_tables, datasets, docs


def save_json(data: dict, filepath: Path):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, default=str, ensure_ascii=False)


def update_data_files(ftp: ftplib.FTP, metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    for dataset in datasets:
        print("Listing data files of", dataset)
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
        metadata_file_path = metadata_dir_path / f"{dataset}.json"
        save_json(data, metadata_file_path)


def list_documentation_files(ftp: ftplib.FTP, dataset: str) -> list[dict]:
    ftp_dir = docs[dataset]["dir"]
    ftp.cwd(ftp_dir)
    files = list_files(ftp, directory=ftp_dir)
    return files


def update_docs(ftp: ftplib.FTP, metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    for doc in docs:
        print("Listing documentation files of", doc)
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
        metadata_file_path = metadata_dir_path / f"{doc}.json"
        save_json(data, metadata_file_path)


def list_auxiliary_tables_files(ftp: ftplib.FTP, dataset: str) -> list[dict]:
    ftp_dir = auxiliary_tables[dataset]["dir"]
    ftp.cwd(ftp_dir)
    files = list_files(ftp, directory=ftp_dir)
    return files


def update_aux(ftp: ftplib.FTP, metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    for aux in auxiliary_tables:
        print("Listing auxiliary files of", aux)
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
        metadata_file_path = metadata_dir_path / f"{aux}.json"
        save_json(data, metadata_file_path)


def get_partition_periods(files: list[dict]) -> set[str]:
    periods = set()
    for file in files:
        period = f"{file['partition']['year']}"
        if file["partition"]["month"]:
            period += f"-{file['partition']['month']:0>2}"
        periods.add(period)
    return periods


def update_index(metadata_dir_path: Path):
    metadata_dir_path.mkdir(parents=True, exist_ok=True)
    metadata_index = {
        "data": {},
        "documentation": {},
        "auxiliary": {},
    }

    for metadata_filepath in sorted((metadata_dir_path / "data").glob("*.json")):
        dataset = metadata_filepath.stem
        with open(metadata_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        n_files = len(data)
        total_size = sum(file["size"] for file in data)
        ufs = set(file["partition"]["uf"] for file in data)
        n_partition_ufs = len(ufs)
        partition_periods = get_partition_periods(data)
        first_period = min(partition_periods) if partition_periods else None
        last_period = max(partition_periods) if partition_periods else None
        n_partition_periods = len(partition_periods)
        if all(len(date) == 7 for date in partition_periods):
            partition_periodicity = "monthly"
        else:
            partition_periodicity = "yearly"
        latest_update = max(file["datetime"] for file in data) if data else None
        metadata_index["data"][dataset] = {
            "n_files": n_files,
            "total_size": total_size,
            "partition_n_ufs": n_partition_ufs,
            "partition_period_start": first_period,
            "partition_period_end": last_period,
            "partition_n_periods": n_partition_periods,
            "partition_periodicity": partition_periodicity,
            "latest_update": latest_update,
        }

    for metadata_filepath in sorted(
        (metadata_dir_path / "documentation").glob("*.json")
    ):
        dataset = metadata_filepath.stem
        with open(metadata_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        n_files = len(data)
        total_size = sum(file["size"] for file in data)
        latest_update = max(file["datetime"] for file in data)
        metadata_index["documentation"][dataset] = {
            "n_files": n_files,
            "total_size": total_size,
            "latest_update": latest_update,
        }

    for metadata_filepath in sorted((metadata_dir_path / "auxiliary").glob("*.json")):
        dataset = metadata_filepath.stem
        with open(metadata_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        n_files = len(data)
        total_size = sum(file["size"] for file in data)
        latest_update = max(file["datetime"] for file in data)
        metadata_index["auxiliary"][dataset] = {
            "n_files": n_files,
            "total_size": total_size,
            "latest_update": latest_update,
        }

    metadata_index_path = metadata_dir_path / "index.json"
    save_json(metadata_index, metadata_index_path)
