from dataclasses import dataclass
from typing import Dict, List, Tuple

from rapidfuzz import fuzz


@dataclass
class MappingSuggestion:
    system_field: str
    source_column: str | None
    confidence: float
    reason: str


def _normalize(value: str) -> str:
    return value.strip().lower().replace("_", " ").replace("-", " ")


def _weighted_score(source_col: str, candidate: str) -> float:
    return max(
        fuzz.ratio(source_col, candidate),
        fuzz.partial_ratio(source_col, candidate),
        fuzz.token_set_ratio(source_col, candidate),
    )


def suggest_mappings(
    source_columns: List[str],
    aliases: Dict[str, List[str]],
    threshold: float = 75,
) -> Dict[str, MappingSuggestion]:
    suggestions: Dict[str, MappingSuggestion] = {}
    normalized_columns = {col: _normalize(col) for col in source_columns}

    for system_field, candidates in aliases.items():
        best: Tuple[str | None, float] = (None, 0.0)
        normalized_candidates = [_normalize(c) for c in candidates + [system_field]]

        for original_col, normalized_col in normalized_columns.items():
            score = max(_weighted_score(normalized_col, cand) for cand in normalized_candidates)
            if score > best[1]:
                best = (original_col, float(score))

        chosen_col, score = best
        if chosen_col and score >= threshold:
            suggestions[system_field] = MappingSuggestion(
                system_field=system_field,
                source_column=chosen_col,
                confidence=score,
                reason=f"Auto-matched with confidence {score:.1f}",
            )
        else:
            suggestions[system_field] = MappingSuggestion(
                system_field=system_field,
                source_column=None,
                confidence=score,
                reason="Low confidence match. Please map manually.",
            )

    return suggestions


def to_manual_mapping_payload(
    suggestions: Dict[str, MappingSuggestion], source_columns: List[str]
) -> List[dict]:
    return [
        {
            "system_field": suggestion.system_field,
            "suggested_column": suggestion.source_column,
            "confidence": suggestion.confidence,
            "reason": suggestion.reason,
            "select_options": ["-- Unmapped --", *source_columns],
            "ui_control": "dropdown_or_dragdrop",
        }
        for suggestion in suggestions.values()
    ]
