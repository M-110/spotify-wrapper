"""
Build the Spotify API class
"""
import os
from typing import Dict, List

import yaml
import pprint

HEADER_TEMPLATE = 'class {class_name}Object(SpotifyObject):'
REPR_HEADER = 'def __repr__(self):'
PROPERTY_TEMPLATE = '@property\ndef {attr_name}(self) -> {attr_return}:'


def create_yaml_dicts(directory: str) -> List[dict]:
    yaml_path = os.path.join(directory, 'object_library.yaml')
    with open(yaml_path, encoding='utf8') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.Loader)


def build(directory: str):
    yaml_dicts = create_yaml_dicts('directory')
    for class_dict in yaml_dicts:
        header = HEADER_TEMPLATE.format(class_dict['name'])
        class_docstring = create_docstring(class_dict['doc'], indent_level=1)

        property_code = []
        for attr in class_dict['attrs']:
            property_declaration = PROPERTY_TEMPLATE.format(
                attr_name=attr['name'],
                attr_return=attr['return'])
            property_docstring = create_docstring(attr['doc'])
            return_statement = parse_return_type(attr['return'], attr['name'])
            code_text = '\n'.join([property_declaration, property_docstring, return_statement])
            property_code.append(code_text)


build('\\test\\')
