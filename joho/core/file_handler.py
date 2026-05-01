import pandas as pd
from pathlib import Path
from dataclasses import fields, asdict
from joho.core.models.anime_model import AnimeDataModel


class DataIO:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    def save_data(self, new_data: AnimeDataModel, overwrite: bool = False) -> None:
        df_new_data = pd.DataFrame([asdict(new_data)])
        if overwrite:
            df_new_data.to_csv(self.filepath, index=False)
            return
        df_previous_data = self._read_file()
        df_merged_data = pd.concat([df_previous_data, df_new_data], ignore_index=True)
        df_merged_data.to_csv(self.filepath, index=False)

    def _read_file(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.filepath)
        except pd.errors.EmptyDataError:
            return self._get_empty_dataframe_model(AnimeDataModel)
        except FileNotFoundError:
            self._get_empty_dataframe_model(AnimeDataModel).to_csv(
                self.filepath, index=False
            )
            return pd.read_csv(self.filepath)

    def _get_empty_dataframe_model(self, model: type[AnimeDataModel]) -> pd.DataFrame:
        return pd.DataFrame(columns=[f.name for f in fields(model)])
