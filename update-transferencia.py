import shutil
from pathlib import Path
from typing import Any

from datasus_metadata.storage import save_json
from datasus_metadata.transferencia import api
from datasus_metadata.transferencia.extract import (
    extract_abrangencia_br,
    extract_abrangencia_todos,
    extract_abrangencia_uf,
    extract_ano_mapa,
    extract_arquivos,
    extract_fonte,
    extract_fontes_anuais,
    extract_modadalidade_datasus,
    extract_modadalidade_territorial,
    extract_modalidade,
    extract_programas_datasus,
    extract_tipo_arquivo,
)


def load_transferenciajs(transferencia_dir: Path):
    transferenciajs_filepath = transferencia_dir / "transferencia.js"

    transferenciajs = api.get_transferenciajs()
    with open(transferenciajs_filepath, "w", encoding="utf-8") as f:
        f.write(transferenciajs)

    return transferenciajs


def remove_links(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for item in data:
        item.pop("link", None)
    return data


def main():
    dest_dir = Path("transferencia")
    shutil.rmtree(dest_dir, ignore_errors=True)
    dest_dir.mkdir(exist_ok=True)

    transferenciajs = load_transferenciajs(dest_dir)

    fontes = extract_fonte(transferenciajs)
    fontes_anuais = extract_fontes_anuais(transferenciajs)
    programas_datasus = extract_programas_datasus(transferenciajs)
    modalidades = extract_modalidade(transferenciajs)
    modadalidades_datasus = extract_modadalidade_datasus(transferenciajs)
    modadalidades_territorial = extract_modadalidade_territorial(transferenciajs)
    arquivos = extract_arquivos(transferenciajs)
    tipo_arquivo = extract_tipo_arquivo(transferenciajs)
    ano_mapa = extract_ano_mapa(transferenciajs)
    abrangencia_br = extract_abrangencia_br(transferenciajs)
    abrangencia_uf = extract_abrangencia_uf(transferenciajs)
    abrangencia_todos = extract_abrangencia_todos(transferenciajs)
    years = list(map(str, range(1979, 2024 + 1)))
    months = list(map(lambda x: f"{x:02d}", range(1, 12 + 1)))

    save_json(fontes, dest_dir / "fontes.json")
    save_json(fontes_anuais, dest_dir / "fontes_anuais.json")
    save_json(programas_datasus, dest_dir / "programas_datasus.json")
    save_json(modalidades, dest_dir / "modalidades.json")
    save_json(modadalidades_datasus, dest_dir / "modadalidades_datasus.json")
    save_json(modadalidades_territorial, dest_dir / "modadalidades_territorial.json")
    save_json(arquivos, dest_dir / "arquivos.json")
    save_json(tipo_arquivo, dest_dir / "tipo_arquivo.json")
    save_json(ano_mapa, dest_dir / "ano_mapa.json")
    save_json(abrangencia_br, dest_dir / "abrangencia_br.json")
    save_json(abrangencia_uf, dest_dir / "abrangencia_uf.json")
    save_json(abrangencia_todos, dest_dir / "abrangencia_todos.json")

    dest_dir = Path("transferencia", "arquivos")
    for arquivo in arquivos:
        if arquivo["fonte"].lower().endswith("_p"):
            continue
        dest_filepath = dest_dir / f"{arquivo['fonte']}-{arquivo['sigla_arquivo']}.json"
        metadados = api.get_arquivos_metadata(
            dataset_abbr=arquivo["sigla_arquivo"],
            dataset_source=arquivo["fonte"],
            years=years,
            months=months,
            ufs=abrangencia_todos,
        )
        metadados = remove_links(metadados)
        if metadados:
            save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "documentacao")
    for fonte in fontes:
        dest_filepath = dest_dir / f"{fonte['sigla']}.json"
        metadados = api.get_documentacao_metadata(dataset_source=fonte["sigla"])
        metadados = remove_links(metadados)
        if metadados:
            save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "auxiliares")
    for fonte in fontes:
        dest_filepath = dest_dir / f"{fonte['sigla']}.json"
        metadados = api.get_auxiliares_metadata(dataset_source=fonte["sigla"])
        metadados = remove_links(metadados)
        if metadados:
            save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "programas-datasus")
    for programa in programas_datasus:
        dest_filepath = dest_dir / f"{programa['sigla_arquivo']}.json"
        metadados = api.get_programas_datasus_metadata(
            tipo_arquivo=programa["sigla_arquivo"],
        )
        metadados = remove_links(metadados)
        if metadados:
            save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "base-territorial")
    dest_filepath = dest_dir / "base-territorial.json"
    metadados = api.get_bases_territoriais_metadata()
    metadados = remove_links(metadados)
    if metadados:
        save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "mapas")
    dest_filepath = dest_dir / "mapas.json"
    metadados = api.get_mapas_metadata(years=ano_mapa, ufs=abrangencia_todos)
    metadados = remove_links(metadados)
    if metadados:
        save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "conversoes")
    dest_filepath = dest_dir / "conversoes.json"
    metadados = api.get_conversoes_metadata(ufs=abrangencia_todos)
    metadados = remove_links(metadados)
    if metadados:
        save_json(metadados, dest_filepath)


if __name__ == "__main__":
    main()
