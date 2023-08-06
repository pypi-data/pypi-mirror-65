from typing import Dict


def format_header_string(header_string: str) -> Dict[str, str]:
    header_dict = {}
    for line in header_string.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip():
            header_dict[key.strip()] = value.strip()
    return header_dict
