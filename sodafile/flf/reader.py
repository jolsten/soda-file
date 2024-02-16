from typing import Dict, List


def unwrap_sections(text: str) -> List[str]:
    unwrapped = []
    current = ""
    for line in text.splitlines():
        if line[0] != " ":
            # If new section found, add completed section to list
            if current:
                unwrapped.append(current)

            # Grab new section
            current = line.rstrip()
        else:
            current += " " + line.strip()

    # If EOF, add the last in-progress line
    if current:
        unwrapped.append(current)

    # Convert to tuple of (label, data)
    tuples = []
    for item in unwrapped:
        name, data = item.split(maxsplit=1)
        tuples.append((name.strip(), data.strip()))
    return tuples


def kvps_to_dict(text: str) -> Dict[str, str]:
    data = {}
    for kvp in text.split():
        key, val = kvp.split("=", maxsplit=1)
        data[key] = val
    return data


def dict_to_kvps(data: Dict[str, str]) -> str:
    return " ".join([f"{key}={val}" for key, val in data.items()])


def parse_text(text: str) -> Dict[str, str]:
    new_tuples = []
    for name, data in unwrap_sections(text):
        new_tuples.append((name, kvps_to_dict(data)))
    return new_tuples
