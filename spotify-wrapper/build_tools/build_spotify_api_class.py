"""
Build the Spotify API class
"""
import os
from typing import Dict, List

import yaml

HEADER_TEMPLATE = 'class {class_name}Object(SpotifyObject):\n'
REPR_HEADER = '\ndef __repr__(self):\n'
PROPERTY_TEMPLATE = '\n@property\ndef {attr_name}(self) -> {attr_return}:\n'


def create_yaml_dicts(directory: str) -> List[dict]:
    yaml_path = os.path.join(directory, 'object_library.yaml')
    with open(yaml_path, encoding='utf8') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.Loader)


def create_docstring(text: str) -> str:
    ...


def create_repr_return(class_name: str, return_types: List[str]) -> str:
    ...


def parse_return_type(return_type, attr_name) -> str:
    ...


def build(directory: str):
    yaml_dicts = create_yaml_dicts('directory')
    for class_dict in yaml_dicts:
        header = HEADER_TEMPLATE.format(class_dict['name'])
        class_docstring = create_docstring(class_dict['doc'])
        REPR_HEADER
        repr_return_statement = create_repr_return(class_dict['name'],
                                                   class_dict['repr_return'])
        property_code = []
        for attr in class_dict['attrs']:
            property_declaration = PROPERTY_TEMPLATE.format(
                attr_name=attr['name'],
                attr_return=attr['return'])
            property_docstring = create_docstring(attr['doc'])
            return_statement = parse_return_type(attr['return'], attr['name'])
            code_text = '\n'.join([property_declaration,
                                   property_docstring,
                                   return_statement])
            property_code.append(code_text)
        class_code = header + class_docstring + '\n'.join(property_code)
        print(class_code)
        break


build('\\test\\')
