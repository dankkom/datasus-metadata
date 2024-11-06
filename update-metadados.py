from pathlib import Path

from datasus_metadados import update


if __name__ == "__main__":
    try:
        update(Path("metadados.json"))
    except Exception as e:
        print("An error occurred:", e)
