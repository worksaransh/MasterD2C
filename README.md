# Upload + Mapping Engine (Focused)

This update focuses only on upload + mapping flows:

1. Auto column detection (fuzzy)
2. Missing required-column detection + user-friendly errors
3. Manual mapping UI (dropdown; can be upgraded to drag/drop)
4. Save reusable mapping templates
5. Shopify + Meta Ads real export column handling

## Supported file types
- `.csv`
- `.xlsx`

## Run UI
```bash
pip install -r requirements.txt
streamlit run mapping_ui.py
```

## Core behavior
- Fuzzy matching uses multiple similarity methods to map uploaded columns to system fields.
- Missing required fields produce explicit errors such as:
  - `Missing required field: PINCODE`
- Manual mapping UI exposes each system field with selectable source columns.
- Saved templates are fingerprinted by source type + column set for auto-reuse.


## Dashboard
```bash
streamlit run dashboard_ui.py
```
- Shows Revenue, Spend, ROAS
- Shows Product-wise, City-wise, and Pincode-wise performance
- Supports filters: Date, Product, Campaign, City, Pincode
