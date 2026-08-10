from pathlib import Path
import json
from typing import List, Dict

DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return "File Path not exist"

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_all_products() -> List[Dict]:
    return load_products()