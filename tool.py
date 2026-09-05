import json
import os
import re

_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.jsonl")

def _load_entries():
    if not os.path.exists(_DATA_PATH):
        return []
    entries = []
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries

_ENTRIES = None

def get_entries():
    global _ENTRIES
    if _ENTRIES is None:
        _ENTRIES = _load_entries()
    return _ENTRIES

def get_entry_by_label(label):
    for e in get_entries():
        if e.get("label") == label:
            return e
    return None

def validate(pattern, text):
    try:
        return re.match(pattern, text) is not None
    except re.error:
        return False

def validate_label(label, text):
    entry = get_entry_by_label(label)
    if entry is None:
        return False
    return validate(entry["input"], text)

def get_labels():
    return [e["label"] for e in get_entries()]

def search_entries(keyword):
    results = []
    kw = keyword.lower()
    for e in get_entries():
        if (kw in e.get("label", "").lower() or
            kw in e.get("note", "").lower() or
            kw in e.get("input", "").lower()):
            results.append(e)
    return results