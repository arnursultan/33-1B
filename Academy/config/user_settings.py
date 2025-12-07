import json
import os

SETTINGS_FILE = os.path.join("config", "user_settings.json")


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"animation": "slide_fade", "theme": "dark"}

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(data: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
