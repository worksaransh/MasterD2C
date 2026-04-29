from typing import Dict, List


def detect_missing_required_fields(mapping: Dict[str, str | None], required_fields: List[str]) -> List[str]:
    return [field for field in required_fields if not mapping.get(field)]


def build_missing_field_messages(missing_fields: List[str]) -> List[str]:
    if not missing_fields:
        return []
    return [
        "These fields are missing. Please map or upload additional data.",
        *[f"Missing required field: {field}" for field in missing_fields],
    ]
