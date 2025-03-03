import json
import re


def extract_fonte(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"fonte = (\[.*?\])", re.M + re.DOTALL)
    fonte_match = pattern.search(transferenciajs)
    if fonte_match:
        raw_json = fonte_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("sigla", '"sigla"')
        raw_json = raw_json.replace("descricao", '"descricao"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_fontes_anuais(transferenciajs: str) -> list[str]:
    pattern = re.compile(r"fontes_anuais = (\[.*?\])", re.M + re.DOTALL)
    fontes_anuais_match = pattern.search(transferenciajs)
    if fontes_anuais_match:
        raw_json = fontes_anuais_match.group(1)
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_programas_datasus(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"programasDatasus = (\[.*?\])", re.M + re.DOTALL)
    programas_datasus_match = pattern.search(transferenciajs)
    if programas_datasus_match:
        raw_json = programas_datasus_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("sigla_arquivo", '"sigla_arquivo"')
        raw_json = raw_json.replace("desc_arquivo", '"desc_arquivo"')
        raw_json = raw_json.replace("abrangencia", '"abrangencia"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_modalidade(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"modadalidade = (\[.*?\])", re.M + re.DOTALL)
    modalidade_match = pattern.search(transferenciajs)
    if modalidade_match:
        raw_json = modalidade_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("codigo", '"codigo"')
        raw_json = raw_json.replace("descricao", '"descricao"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_modalidade_datasus(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"modadalidadeDATASUS = (\[.*?\])", re.M + re.DOTALL)
    modadalidade_datasus_match = pattern.search(transferenciajs)
    if modadalidade_datasus_match:
        raw_json = modadalidade_datasus_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("codigo", '"codigo"')
        raw_json = raw_json.replace("descricao", '"descricao"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_modalidade_territorial(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"modadalidadeTerritorial = (\[.*?\])", re.M + re.DOTALL)
    modadalidade_territorial_match = pattern.search(transferenciajs)
    if modadalidade_territorial_match:
        raw_json = modadalidade_territorial_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("codigo", '"codigo"')
        raw_json = raw_json.replace("descricao", '"descricao"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_arquivos(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"arquivo = (\[.*?\])", re.M + re.DOTALL)
    arquivos_match = pattern.search(transferenciajs)
    if arquivos_match:
        raw_json = arquivos_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("fonte", '"fonte"')
        raw_json = raw_json.replace("sigla_arquivo", '"sigla_arquivo"')
        raw_json = raw_json.replace("desc_arquivo", '"desc_arquivo"')
        raw_json = raw_json.replace("abrangencia", '"abrangencia"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_tipo_arquivo(transferenciajs: str) -> list[dict]:
    pattern = re.compile(r"tipo_arquivo = (\[.*?\])", re.M + re.DOTALL)
    tipo_arquivo_match = pattern.search(transferenciajs)
    if tipo_arquivo_match:
        raw_json = tipo_arquivo_match.group(1)
        # Quote keys
        raw_json = raw_json.replace("sigla_arquivo", '"sigla_arquivo"')
        raw_json = raw_json.replace("desc_arquivo", '"desc_arquivo"')
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_ano_mapa(transferenciajs: str) -> list[int]:
    pattern = re.compile(r"ano_mapa = (\[.*?\])", re.M + re.DOTALL)
    ano_mapa_match = pattern.search(transferenciajs)
    if ano_mapa_match:
        raw_json = ano_mapa_match.group(1)
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_abrangencia_br(transferenciajs: str) -> list[str]:
    pattern = re.compile(r"abrag_br = (\[.*?\])", re.M + re.DOTALL)
    abrangencia_br_match = pattern.search(transferenciajs)
    if abrangencia_br_match:
        raw_json = abrangencia_br_match.group(1)
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_abrangencia_uf(transferenciajs: str) -> list[str]:
    pattern = re.compile(r"abrag_uf = (\[.*?\])", re.M + re.DOTALL)
    abrangencia_uf_match = pattern.search(transferenciajs)
    if abrangencia_uf_match:
        raw_json = abrangencia_uf_match.group(1)
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []


def extract_abrangencia_todos(transferenciajs: str) -> list[str]:
    pattern = re.compile(r"abrag_todos = (\[.*?\])", re.M + re.DOTALL)
    abrangencia_todos_match = pattern.search(transferenciajs)
    if abrangencia_todos_match:
        raw_json = abrangencia_todos_match.group(1)
        # Remove last comma inside array
        raw_json = re.sub(r"}\s*,\s*]\s*$", "}]", raw_json, flags=re.DOTALL)
        return json.loads(raw_json)
    return []
