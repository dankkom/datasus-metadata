import datetime as dt
import ftplib
import time
from functools import lru_cache

from . import logger, meta
from .remote_files import DataPartition, RemoteFile, get_pattern, parse_filename

FTP_HOST = "ftp.datasus.gov.br"
MEGA = 1_000_000


def connect() -> ftplib.FTP:
    """Connects to the FTP server."""
    ftp = ftplib.FTP(FTP_HOST, encoding="latin-1")
    ftp.login()
    return ftp


@lru_cache
def list_files(
    ftp: ftplib.FTP,
    directory: str,
    retries: int = 3,
) -> list[dict]:
    try:
        ftp.cwd(directory)
    except ftplib.error_perm:
        logger.exception(f"Directory not found. {directory}")

    files: list[str] = []
    while retries > 0:
        files.clear()
        try:
            ftp.retrlines("LIST", files.append)
            break
        # Timeout exception
        except (ftplib.error_temp, TimeoutError):
            logger.exception("Timeout exception while listing files.")
            retries -= 1
            time.sleep(5)

    # parse files' date, size and name
    def parse_line(line: str) -> dict[str, str | int | dt.datetime | None]:
        date, time, size, name = line.split(maxsplit=3)
        extension = name.rsplit(".", maxsplit=1)[1].lower()
        datetime = dt.datetime.strptime(date + " " + time, "%m-%d-%y %I:%M%p")
        try:
            size = int(size)
        except ValueError:
            size = None
        return {
            "datetime": datetime,
            "size": size,
            "filename": name,
            "extension": extension,
            "full_path": f"{directory}/{name}",
        }

    parsed_files = [parse_line(line) for line in files]

    return parsed_files


def list_dataset_files(ftp: ftplib.FTP, dataset: str) -> list[RemoteFile]:
    dataset_files = []
    for period in meta.datasets[dataset]["periods"]:
        files = [
            RemoteFile(
                filename=f["filename"],
                datetime=f["datetime"],
                size=f["size"],
                extension=f["extension"],
                full_path=f["full_path"],
                dataset=dataset,
                preliminary=period.get("preliminary", False),
            )
            for f in list_files(ftp, directory=period["dir"], retries=3)
        ]
        if not period["filename_pattern"]:
            dataset_files.extend(files)
            continue
        fn_pattern = period["filename_pattern"]
        pattern = get_pattern(period=period)
        for file in files:
            m = pattern.match(file.filename.lower())
            if m:
                file.partition = DataPartition(**parse_filename(m, fn_pattern))
                dataset_files.append(file)
    return dataset_files


def list_documentation_files(ftp: ftplib.FTP, dataset: str) -> list[RemoteFile]:
    ftp_dir = meta.docs[dataset]["dir"]
    ftp.cwd(ftp_dir)
    files = list_files(ftp, directory=ftp_dir)
    documentation_files = []
    for file in files:
        documentation_files.append(
            RemoteFile(
                filename=file["filename"],
                full_path=file["full_path"],
                datetime=file["datetime"],
                extension=file["extension"],
                size=file["size"],
                dataset=dataset,
            )
        )
    return documentation_files


def list_auxiliary_tables_files(ftp: ftplib.FTP, dataset: str) -> list[RemoteFile]:
    ftp_dir = meta.auxiliary_tables[dataset]["dir"]
    ftp.cwd(ftp_dir)
    files = list_files(ftp, directory=ftp_dir)
    auxiliary_files = []
    for file in files:
        auxiliary_files.append(
            RemoteFile(
                filename=file["filename"],
                full_path=file["full_path"],
                datetime=file["datetime"],
                extension=file["extension"],
                size=file["size"],
                dataset=dataset,
            )
        )
    return auxiliary_files
