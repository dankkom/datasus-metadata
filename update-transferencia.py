import json
import time
from pathlib import Path

from datasus_metadata.transferencia.extract import (
    extract_fonte,
    extract_fontes_anuais,
    extract_programas_datasus,
    extract_modalidade,
    extract_modadalidade_datasus,
    extract_modadalidade_territorial,
    extract_arquivos,
    extract_tipo_arquivo,
    extract_ano_mapa,
    extract_abrangencia_br,
    extract_abrangencia_uf,
    extract_abrangencia_todos,
)
from datasus_metadata.transferencia import api


def load_transferenciajs():
    transferenciajs_filepath = Path("transferencia", "transferencia.js")
    file_exists = transferenciajs_filepath.exists()
    is_old = transferenciajs_filepath.stat().st_mtime < time.time() - 60 * 60 * 24
    if not file_exists or is_old:
        transferenciajs = api.get_transferenciajs()
        with open(transferenciajs_filepath, "w", encoding="utf-8") as f:
            f.write(transferenciajs)
    else:
        with open(transferenciajs_filepath, "r", encoding="utf-8") as f:
            transferenciajs = f.read()
    return transferenciajs


def save_json(data, filepath: Path):
    print("Saving JSON:", filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    transferenciajs = load_transferenciajs()

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

    dest_dir = Path("transferencia")
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
        # if dest_filepath.exists():
        #     continue
        metadados = api.get_arquivos_metadata(
            dataset_abbr=arquivo["sigla_arquivo"],
            dataset_source=arquivo["fonte"],
            years=years,
            months=months,
            ufs=abrangencia_todos,
        )
        save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "documentacao")
    for fonte in fontes:
        dest_filepath = dest_dir / f"{fonte['sigla']}.json"
        metadados = api.get_documentacao_metadata(dataset_source=fonte["sigla"])
        save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "auxiliares")
    for fonte in fontes:
        dest_filepath = dest_dir / f"{fonte['sigla']}.json"
        metadados = api.get_auxiliares_metadata(dataset_source=fonte["sigla"])
        save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "programas-datasus")
    for programa in programas_datasus:
        dest_filepath = dest_dir / f"{programa['sigla_arquivo']}.json"
        metadados = api.get_programas_datasus_metadata(
            tipo_arquivo=programa["sigla_arquivo"],
        )
        save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "base-territorial")
    dest_filepath = dest_dir / "base-territorial.json"
    metadados = api.get_bases_territoriais_metadata()
    save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "mapas")
    dest_filepath = dest_dir / "mapas.json"
    metadados = api.get_mapas_metadata(years=ano_mapa, ufs=abrangencia_todos)
    save_json(metadados, dest_filepath)

    dest_dir = Path("transferencia", "conversoes")
    dest_filepath = dest_dir / "conversoes.json"
    metadados = api.get_conversoes_metadata(ufs=abrangencia_todos)
    save_json(metadados, dest_filepath)


if __name__ == "__main__":
    main()
