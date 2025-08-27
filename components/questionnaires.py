import json, os

def load_dass21_vi():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "dass21_vi.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
