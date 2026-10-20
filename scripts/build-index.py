from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
packs_dir = root / "packs"
packs_dir.mkdir(exist_ok=True)

index_path = root / "index.json"
if index_path.exists():
    try:
        old_index = json.loads(index_path.read_text(encoding="utf-8-sig"))
    except Exception:
        old_index = {}
    for entry in old_index.get("packs", []):
        pack_id = str(entry.get("id", "")).strip()
        if not pack_id:
            continue
        safe_id = re.sub(r"[^A-Za-z0-9._-]+", "-", pack_id).strip("-") or "pack"
        path = packs_dir / f"{safe_id}.json"
        if not path.exists():
            path.write_text(
                json.dumps(entry, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )

entries = []

for path in sorted(packs_dir.glob("*.json")):
    try:
        entry = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}")

    if not isinstance(entry, dict) or not entry.get("id"):
        raise SystemExit(f"{path}: entry must be an object with an id")

    entries.append(entry)

entries.sort(key=lambda item: str(item["id"]).lower())
index = {"schemaVersion": 2, "packs": entries}
text = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
(root / "index.json").write_text(text, encoding="utf-8", newline="\n")
print(f"Wrote index.json with {len(entries)} pack(s)")
