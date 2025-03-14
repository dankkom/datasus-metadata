import json
import time
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

URL = "https://datasus.saude.gov.br/wp-content/ftp.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
TIMEOUT = 300


def request_post(payload: dict[str, Any], retries: int = 3) -> Any:
    req = Request(URL, headers=HEADERS)
    req.data = urlencode(payload, doseq=True).encode("utf-8")
    req.method = "POST"

    for _ in range(retries):
        try:
            response = urlopen(req, timeout=TIMEOUT)
            response_json = json.loads(response.read())
            break
        except HTTPError as e:
            if e.code == 504:
                print("Gateway Timeout. Retrying in 5 seconds...")
                time.sleep(5)
                continue

    if response_json is None:
        raise Exception("Failed to fetch metadata")

    return response_json


def get_transferenciajs() -> str:
    transferencia_url = "https://datasus.saude.gov.br/wp-content/transferencia.js"
    req = Request(transferencia_url)
    response = urlopen(req, timeout=TIMEOUT)
    data = response.read()

    return data.decode("utf-8")


def get_auxiliares_metadata(dataset_source: str) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "AUX",
        "modalidade[]": "0",
        "fonte[]": dataset_source,
    }

    response_json = request_post(payload_dict)

    return response_json


def get_arquivos_metadata(
    dataset_abbr: str,
    dataset_source: str,
    years: list[str],
    months: list[str],
    ufs: list[str],
) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": dataset_abbr,
        "modalidade[]": "1",
        "fonte[]": dataset_source,
        "ano[]": years,
        "mes[]": months,
        "uf[]": ufs,
    }

    response_json = request_post(payload_dict)

    return response_json


def get_documentacao_metadata(dataset_source: str) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "DOC",
        "modalidade[]": "2",
        "fonte[]": dataset_source,
    }

    response_json = request_post(payload_dict)

    return response_json


def get_programas_datasus_metadata(tipo_arquivo: str) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": tipo_arquivo,
        "modalidade[]": "3",
        "fonte[]": "DATASUS",
    }

    response_json = request_post(payload_dict)

    return response_json


def get_bases_territoriais_metadata():
    payload_dict = {
        "tipo_arquivo[]": "TER",
        "modalidade[]": "4",
        "fonte[]": "Base Territorial",
    }

    response_json = request_post(payload_dict)

    return response_json


def get_mapas_metadata(years: list[int], ufs: list[str]) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "MAP",
        "modalidade[]": "5",
        "fonte[]": "Base Territorial",
        "ano[]": years,
        "uf[]": ufs,
    }

    response_json = request_post(payload_dict)

    return response_json


def get_conversoes_metadata(ufs: list[str]) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "CNV",
        "modalidade[]": "6",
        "fonte[]": "Base Territorial",
        "uf[]": ufs,
    }

    response_json = request_post(payload_dict)

    return response_json
