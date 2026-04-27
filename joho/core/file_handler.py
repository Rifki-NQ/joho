import pandas as pd
from pathlib import Path
from dataclasses import fields, asdict
from argparse import ArgumentTypeError
from joho.core.models.anime_model import AnimeDataModel


# filepath validation for argparse --path
def valid_filepath(filepath: str) -> Path:
    filepath = filepath.strip().replace(" ", "_")
    filepath_folder = str(Path(filepath).parent)
    if filepath_folder != "storage":
        raise ArgumentTypeError(
            "dataset file must be in the designated folder (example: storage/file.csv)"
        )
    if not filepath.lower().endswith(".csv"):
        raise ArgumentTypeError(
            "dataset file must be a csv file (example: storage/file.csv)"
        )
    return Path(filepath)


class DataIO:
    def save_data(
        self, new_data: AnimeDataModel, filepath: Path, overwrite: bool = False
    ) -> None:
        df_new_data = pd.DataFrame([asdict(new_data)])
        if overwrite:
            df_new_data.to_csv(filepath, index=False)
            return
        df_previous_data = self._read_file(filepath)
        df_merged_data = pd.concat([df_previous_data, df_new_data], ignore_index=True)
        df_merged_data.to_csv(filepath, index=False)

    def _read_file(self, filepath: Path) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except pd.errors.EmptyDataError:
            return self._get_empty_dataframe_model(AnimeDataModel)
        except FileNotFoundError:
            # cli guarantee the file is in storage/
            self._get_empty_dataframe_model(AnimeDataModel).to_csv(
                filepath, index=False
            )
            return pd.read_csv(filepath)

    def _get_empty_dataframe_model(self, model: type[AnimeDataModel]) -> pd.DataFrame:
        return pd.DataFrame(columns=[f.name for f in fields(model)])
