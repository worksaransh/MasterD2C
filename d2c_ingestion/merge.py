import pandas as pd


def merge_datasets(orders: pd.DataFrame, ads: pd.DataFrame, shipments: pd.DataFrame) -> pd.DataFrame:
    merged = orders.copy()

    for key in ["ORDER_ID", "ORDER_DATE", "SKU", "CAMPAIGN_NAME"]:
        if key not in merged.columns:
            merged[key] = pd.NA

    if "CAMPAIGN_NAME" in ads.columns:
        merged = merged.merge(ads, how="left", on=[c for c in ["ORDER_DATE", "CAMPAIGN_NAME"] if c in ads.columns and c in merged.columns], suffixes=("", "_ads"))

    if "ORDER_ID" in shipments.columns:
        merged = merged.merge(shipments, how="left", on=[c for c in ["ORDER_ID", "SKU"] if c in shipments.columns and c in merged.columns], suffixes=("", "_ship"))

    return merged
