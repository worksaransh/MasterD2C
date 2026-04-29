from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


def read_upload(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path)
