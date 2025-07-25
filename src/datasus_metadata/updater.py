import ftplib
import shutil
from pathlib import Path

from .fetcher import list_dataset_files, list_files
from .meta import auxiliary_tables, datasets, datasets_sources, docs
from .storage import load_json, save_json


def update_data_files(ftp: ftplib.FTP, metadata_dir_path: Path):
    shutil.rmtree(metadata_dir_path, ignore_errors=True)
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
                        "subpartition": remote_file.partition.subpartition,
                    },
                    "preliminary": remote_file.preliminary,
                }
            )
        data = sorted(
            data,
            key=lambda x: (
                x["partition"]["year"],
                x["partition"]["month"],
                x["partition"]["uf"],
                x["partition"]["subpartition"],
            ),
        )
        metadata_file_path = metadata_dir_path / f"{dataset}.json"
        save_json(data, metadata_file_path)


def list_documentation_files(ftp: ftplib.FTP, dataset: str) -> list[dict]:
    files = []
    for ftp_dir in docs[dataset]["dir"]:
        ftp.cwd(ftp_dir)
        files.extend(list_files(ftp, directory=ftp_dir))
    return files


def update_docs(ftp: ftplib.FTP, metadata_dir_path: Path):
    shutil.rmtree(metadata_dir_path, ignore_errors=True)
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
    files = []
    for ftp_dir in auxiliary_tables[dataset]["dir"]:
        ftp.cwd(ftp_dir)
        files.extend(list_files(ftp, directory=ftp_dir))
    return files


def update_aux(ftp: ftplib.FTP, metadata_dir_path: Path):
    shutil.rmtree(metadata_dir_path, ignore_errors=True)
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
        if not file["partition"]["year"]:
            continue
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
        slug = metadata_filepath.stem
        name = datasets[slug]["name"]
        source = datasets[slug]["source"]
        data = load_json(metadata_filepath)
        n_files = len(data)
        total_size = sum(file["size"] for file in data)
        ufs = set(file["partition"]["uf"] for file in data)
        n_partition_ufs = len(ufs)
        partition_periods = get_partition_periods(data)
        first_period = min(partition_periods) if partition_periods else None
        last_period = max(partition_periods) if partition_periods else None
        n_partition_periods = len(partition_periods)
        dataset_partition = datasets[slug]["partition"]
        partition_periodicity = None
        if "year" in dataset_partition:
            partition_periodicity = "yearly"
        if "yearmonth" in dataset_partition:
            partition_periodicity = "monthly"
        latest_update = max(file["datetime"] for file in data) if data else None
        metadata_index["data"][slug] = {
            "name": name,
            "source": source,
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
        slug = metadata_filepath.stem
        source_name = datasets_sources.get(slug, {}).get("name")
        data = load_json(metadata_filepath)
        n_files = len(data)
        total_size = sum(file["size"] for file in data)
        latest_update = max(file["datetime"] for file in data)
        metadata_index["documentation"][slug] = {
            "source_name": source_name,
            "n_files": n_files,
            "total_size": total_size,
            "latest_update": latest_update,
        }

    for metadata_filepath in sorted((metadata_dir_path / "auxiliary").glob("*.json")):
        slug = metadata_filepath.stem
        source_name = datasets_sources.get(slug, {}).get("name")
        data = load_json(metadata_filepath)
        n_files = len(data)
        total_size = sum(file["size"] for file in data)
        latest_update = max(file["datetime"] for file in data)
        metadata_index["auxiliary"][slug] = {
            "source_name": source_name,
            "n_files": n_files,
            "total_size": total_size,
            "latest_update": latest_update,
        }

    metadata_index_path = metadata_dir_path / "index.json"
    save_json(metadata_index, metadata_index_path)
