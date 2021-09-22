import ujson
from pathlib import Path
from typing import Union


def safe_read_file(filename: Union[Path, str]) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f'File {filename} not found')
        exit()


def check_dict_schema(obj: dict, required_keys: dict):
    for name, _type in required_keys.items():
        value = obj.get(name)
        assert value is not None, f'`{obj}` does not have a required field `{name}`'
        assert type(value) == _type, f'`{obj}`\nField `{name}` is of type {type(value)} but {_type} is required'


def safe_load_json(data: str, **required_keys):
    """ Loads json and checks if it has required keys.
        required_keys: dict which maps name of key to its type, ex. {name: str}"""
    try:
        loaded = ujson.loads(data)
    except ValueError:
        print(f'Could not read JSON: `{data}`\nPlease check syntax')
        return exit()

    if required_keys:
        if isinstance(loaded, list):
            [check_dict_schema(obj, required_keys) for obj in loaded]
        elif isinstance(loaded, dict):
            check_dict_schema(loaded, required_keys)
    return loaded
