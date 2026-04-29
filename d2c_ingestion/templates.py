from dataclasses import dataclass
from typing import Dict, List


SYSTEM_FIELDS = {
    "ORDER_ID": ["order id", "order_id", "order number", "name"],
    "ORDER_DATE": ["order date", "created at", "date", "day"],
    "REVENUE": ["amount", "total price", "net sales", "gross sales", "revenue"],
    "SPEND": ["ad spend", "amount spent", "spend", "amount_spent_usd"],
    "CITY": ["city", "shipping city", "billing city"],
    "PINCODE": ["pincode", "zip", "postal code", "shipping zip"],
    "CAMPAIGN_NAME": ["campaign", "campaign name", "campaign name (ad set)"],
    "SKU": ["sku", "lineitem sku", "variant sku"],
    "PRODUCT_COST": ["product cost", "cogs", "cost of goods"],
}


@dataclass
class Template:
    name: str
    source_type: str
    required_fields: List[str]
    optional_fields: List[str]
    field_aliases: Dict[str, List[str]]


PREBUILT_TEMPLATES: Dict[str, Template] = {
    "shopify": Template(
        name="Shopify Orders Export",
        source_type="shopify",
        required_fields=["ORDER_ID", "ORDER_DATE", "REVENUE", "SKU"],
        optional_fields=["CITY", "PINCODE"],
        field_aliases=SYSTEM_FIELDS,
    ),
    "meta_ads": Template(
        name="Meta Ads Performance Export",
        source_type="meta_ads",
        required_fields=["CAMPAIGN_NAME", "ORDER_DATE", "SPEND"],
        optional_fields=["REVENUE"],
        field_aliases=SYSTEM_FIELDS,
    ),
}
