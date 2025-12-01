
import json

REQUIRED_KEYS = {
    "name": None,
    "type": None,
    "ip": None,
    "prefix-length": None,
    "in-octets": None,
    "in-unicast-pkts": None,
    "out-octets": None,
    "out-unicast-pkts": None,
}

class MissingKeysError(Exception):
    pass

def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def flatten_dict(data, key):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                REQUIRED_KEYS[k] = v
                return True
            if isinstance(v, (dict, list)):
                if flatten_dict(v, key):
                    return True
    elif isinstance(data, list):
        for item in data:
            if item is not None and flatten_dict(item, key):
                return True
    return False

def extract_keys(data):
    missing_keys = []
    for key in REQUIRED_KEYS:
        if not flatten_dict(data, key):
            missing_keys.append(key)
    return missing_keys

def main():
    file_path = "intf.json"
    data = load_json(file_path)
    missing_keys = extract_keys(data)
    print("Extracted Data:", REQUIRED_KEYS)
    if missing_keys:
        raise MissingKeysError(f"Keys not found: {', '.join(missing_keys)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")