import json
from pathlib import Path

from datasus_fetcher.fetcher import connect, list_dataset_files
from datasus_fetcher.meta import datasets


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
