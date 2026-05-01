import csv
from pathlib import Path
from dataclasses import fields, asdict
from joho.core.models.anime_model import AnimeDataModel


class DataIO:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def save_data(self, data: AnimeDataModel, overwrite: bool) -> None:
        overwrite_map = {True: "w", False: "a"}
        with open(self.filepath, mode=overwrite_map[overwrite], newline="") as f:
            fieldnames = [adm.name for adm in fields(AnimeDataModel)]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if self._is_empty_file():
                writer.writeheader()
            writer.writerow(asdict(data))

    def _is_empty_file(self) -> bool:
        return self.filepath.stat().st_size == 0
