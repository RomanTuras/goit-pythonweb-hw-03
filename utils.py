import os
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

STORAGE_DIR = "storage"
FILE_PATH = os.path.join(STORAGE_DIR, "data.json")

env = Environment(loader=FileSystemLoader("templates"))


def write_json(data):
    """Write data into JSON-file with timestamp."""
    os.makedirs(STORAGE_DIR, exist_ok=True)

    # Reading exists data
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    # Add a new record
    existing_data[datetime.now().isoformat()] = data

    # Write back
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


def read_html(filename):
    """Reading HTML-file from templates folder."""
    path = os.path.join("templates", filename)
    if os.path.exists(path):
        with open(path, "rb") as file:
            return file.read()
    return None


def render_template(template_name, **context):
    """Render HTML-template with props."""
    template = env.get_template(template_name)
    return template.render(context).encode("utf-8")
