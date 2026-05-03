import csv
from pathlib import Path
from dataclasses import fields, asdict
from joho.core.models.anime_model import AnimeDataModel
from joho.core.exceptions import (
    FileNotExistError,
    FileEmptyError,
    MissingHeaderError,
    InvalidHeaderError,
)


class DataIO:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def save_data(self, data: AnimeDataModel, overwrite: bool) -> None:
        overwrite_map = {True: "w", False: "a"}
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        is_empty_file = self._file_empty() if self._file_exist() else True
        with open(self.filepath, mode=overwrite_map[overwrite], newline="") as f:
            fieldnames = [adm.name for adm in fields(AnimeDataModel)]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if overwrite or is_empty_file:
                writer.writeheader()
            writer.writerow(asdict(data))

    def read_data(self) -> list[dict[str, str]]:
        if not self._file_exist():
            raise FileNotExistError("Error: file does not exist")
        elif self._file_empty():
            self._raise_file_empty_error()
        entries: list[dict[str, str]] = []
        with open(self.filepath, mode="r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._validate_headers(row)
                entries.append(row)
        if not entries:
            self._raise_file_empty_error()
        return entries

    def _file_exist(self) -> bool:
        return self.filepath.exists()

    def _file_empty(self) -> bool:
        return self.filepath.stat().st_size == 0

    def _raise_file_empty_error(self) -> None:
        raise FileEmptyError("Error: file is empty")

    def _validate_headers(self, entry_data: dict[str, str]) -> None:
        valid_keys = set(f.name for f in fields(AnimeDataModel))
        actual_keys = entry_data.keys()
        missing_keys: set[str] = valid_keys - actual_keys
        extra_keys: set[str] = actual_keys - valid_keys
        if missing_keys:
            raise MissingHeaderError(
                f"Error: missing header from the file: {missing_keys}"
            )
        if extra_keys:
            raise InvalidHeaderError(f"Error: invalid header: {extra_keys}")
