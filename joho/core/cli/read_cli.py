from joho.core.file_handler import DataIO
from joho.core.exceptions import FileHandlerError


class ReadCLI:
    def __init__(self, file_handler: DataIO) -> None:
        self.file_handler = file_handler

    def handle_read_cli(self, entry: int | None) -> None:
        try:
            all_data = self.file_handler.read_data()
        except FileHandlerError as e:
            print(e)
            return
        if entry is not None:
            try:
                self._show_entry(all_data[entry])
            except IndexError:
                print(
                    f"Error: out of bound entry index: {entry}, for file: {self.file_handler.filepath}"
                )
            return
        self._show_entries(all_data)

    def _show_entry(self, entry_data: dict[str, str]) -> None:
        for key, value in entry_data.items():
            print(f"{key}: {value}")

    def _show_entries(self, data_list: list[dict[str, str]]) -> None:
        for entry in data_list:
            self._show_entry(entry)
            print()
