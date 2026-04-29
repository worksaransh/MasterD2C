from dataclasses import asdict
from typing import Any, Dict

from .cleaning import clean_frame
from .io import read_upload
from .mapping import suggest_mappings, to_manual_mapping_payload
from .templates import PREBUILT_TEMPLATES
from .validation import build_missing_field_messages, detect_missing_required_fields


def _build_standardized_records(cleaned, mapped: Dict[str, str | None]) -> list[dict]:
    standardized = {}
    for system_field, source_col in mapped.items():
        if source_col and source_col in cleaned.columns:
            standardized[system_field] = cleaned[source_col]
    if not standardized:
        return []
    return cleaned.assign(**standardized)[list(standardized.keys())].to_dict(orient="records")


def process_upload(file_path: str, template_key: str, threshold: float = 75) -> Dict[str, Any]:
    template = PREBUILT_TEMPLATES[template_key]
    raw = read_upload(file_path)
    cleaned = clean_frame(raw)

    suggestions = suggest_mappings(cleaned.columns.tolist(), template.field_aliases, threshold=threshold)
    mapped = {k: v.source_column for k, v in suggestions.items()}

    missing_required = detect_missing_required_fields(mapped, template.required_fields)
    missing_messages = build_missing_field_messages(missing_required)

    return {
        "template": template.name,
        "row_count": len(cleaned),
        "columns": cleaned.columns.tolist(),
        "mapping_suggestions": {k: asdict(v) for k, v in suggestions.items()},
        "manual_mapping_ui": to_manual_mapping_payload(suggestions, cleaned.columns.tolist()),
        "missing_required_fields": missing_required,
        "errors": missing_messages,
        "standardized_records": _build_standardized_records(cleaned, mapped),
        "preview": cleaned.head(20).to_dict(orient="records"),
    }
