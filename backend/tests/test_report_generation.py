from pathlib import Path

from app.reports.json_exporter import export_json

def test_json_exporter_persists_valid_json(tmp_path: Path):
    path = tmp_path / "security.json"
    returned = export_json({"status": "Completed", "findings": []}, path)
    assert returned == str(path)
    assert path.is_file()
    assert '"status": "Completed"' in path.read_text(encoding="utf-8")
