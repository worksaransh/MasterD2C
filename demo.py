import json

from d2c_ingestion.pipeline import process_upload


if __name__ == "__main__":
    # Replace with a real file path in your environment.
    # Example: result = process_upload("examples/shopify_orders.csv", "shopify")
    print(json.dumps({
        "status": "ready",
        "message": "Engine scaffolded. Call process_upload(file_path, template_key).",
        "templates": ["shopify", "meta_ads", "google_ads", "shipment", "product_cost"],
    }, indent=2))
