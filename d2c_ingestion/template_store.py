import hashlib
import json
from pathlib import Path
from typing import Dict, List


class TemplateStore:
    def __init__(self, path: str = "saved_templates.json") -> None:
        self.path = Path(path)

    def load(self) -> Dict[str, dict]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def _fingerprint(self, source_type: str, columns: List[str]) -> str:
        joined = f"{source_type}|{'|'.join(sorted(columns))}"
        return hashlib.sha1(joined.encode()).hexdigest()[:12]

    def save_mapping_template(self, name: str, source_type: str, columns: List[str], mapping: Dict[str, str]) -> str:
        data = self.load()
        template_id = self._fingerprint(source_type, columns)
        data[template_id] = {
            "name": name,
            "source_type": source_type,
            "columns": columns,
            "mapping": mapping,
        }
        self.path.write_text(json.dumps(data, indent=2))
        return template_id

    def find_best_template(self, source_type: str, columns: List[str]) -> dict | None:
        data = self.load()
        template_id = self._fingerprint(source_type, columns)
        return data.get(template_id)
