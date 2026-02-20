import json
import os

FILE_PATH = "candidates.json"

def save_candidate(data):
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)

    with open(FILE_PATH, "r") as f:
        existing = json.load(f)

    existing.append(data)

    with open(FILE_PATH, "w") as f:
        json.dump(existing, f, indent=4)
