import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

url = "https://datasus.saude.gov.br/wp-content/ftp.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def get_transferenciajs() -> str:
    transferencia_url = "https://datasus.saude.gov.br/wp-content/transferencia.js"
    req = Request(transferencia_url)
    response = urlopen(req)
    data = response.read()

    return data.decode("utf-8")


def get_auxiliares_metadata(dataset_source: str) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "AUX",
        "modalidade[]": "0",
        "fonte[]": dataset_source,
    }

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

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

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

    return response_json


def get_documentacao_metadata(dataset_source: str) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "DOC",
        "modalidade[]": "2",
        "fonte[]": dataset_source,
    }

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

    return response_json


def get_programas_datasus_metadata(tipo_arquivo: str) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": tipo_arquivo,
        "modalidade[]": "3",
        "fonte[]": "DATASUS",
    }

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

    return response_json


def get_bases_territoriais_metadata():
    payload_dict = {
        "tipo_arquivo[]": "TER",
        "modalidade[]": "4",
        "fonte[]": "Base Territorial",
    }

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

    return response_json


def get_mapas_metadata(years: list[int], ufs: list[str]) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "MAP",
        "modalidade[]": "5",
        "fonte[]": "Base Territorial",
        "ano[]": years,
        "uf[]": ufs,
    }

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

    return response_json


def get_conversoes_metadata(ufs: list[str]) -> list[Any]:
    payload_dict = {
        "tipo_arquivo[]": "CNV",
        "modalidade[]": "6",
        "fonte[]": "Base Territorial",
        "uf[]": ufs,
    }

    payload = urlencode(payload_dict, doseq=True)

    req = Request(url, headers=headers)
    req.data = payload.encode("utf-8")
    req.method = "POST"

    response = urlopen(req)
    response_json = json.loads(response.read())

    return response_json
