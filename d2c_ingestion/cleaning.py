import pandas as pd


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates()

    for col in cleaned.columns:
        if "date" in col.lower():
            cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce", utc=True).dt.date

        if any(token in col.lower() for token in ["amount", "revenue", "spend", "cost", "price"]):
            cleaned[col] = (
                cleaned[col]
                .astype(str)
                .str.replace(r"[^0-9.-]", "", regex=True)
                .replace("", pd.NA)
            )
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    return cleaned.fillna(pd.NA)
