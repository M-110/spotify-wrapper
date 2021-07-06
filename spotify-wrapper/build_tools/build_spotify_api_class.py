"""
Build the Spotify API class
"""
import os
import textwrap
from typing import List

import yaml

HEADER_TEMPLATE = 'class {class_name}Object(SpotifyObject):\n'
PROPERTY_TEMPLATE = '\n@property\ndef {attr_name}(self) -> {attr_return}:'


def create_yaml_dicts(directory: str) -> List[dict]:
    yaml_path = os.path.join(directory, 'object_library.yaml')
    with open(yaml_path, encoding='utf8') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.Loader)


def create_class(class_dict: dict) -> str:
    print(class_dict['name'])
    class_header = HEADER_TEMPLATE.format(class_name=class_dict['name'])
    class_docstring = create_docstring(class_dict['doc'], 1)
    repr_header = '\ndef __repr__(self):\n'
    repr_return_statement = create_repr_return(class_dict)
    property_code = []
    for attr in class_dict['attrs']:
        property_text = create_property(attr)
        property_code.append(property_text)
    class_statement = class_header + class_docstring + '\n\n'
    class_methods = repr_header + repr_return_statement + '\n\n' + \
                    '\n\n'.join(property_code)
    class_methods = textwrap.indent(class_methods, ' ' * 4)
    return class_statement + class_methods


def create_docstring(text: str, indent: int) -> str:
    """Wrap the docstring and surround it with triple quotes."""
    wrapped_text = _wrap_line(text)
    docstring = f'"""\n{wrapped_text}\n"""'
    return textwrap.indent(docstring, prefix=' ' * (4 * indent))


def _wrap_line(line: str) -> str:
    """Wrap the given line and preserve the indent level."""
    line_indent = ' ' * (len(line) - len(line.lstrip()))
    wrapped_lines = [textwrap.fill(cut_line, subsequent_indent=line_indent)
                     for cut_line in line.split('\n')]
    return '\n'.join(wrapped_lines)


def create_repr_return(class_dict: dict) -> str:
    """Create the return line of the repr method which will display a few
    of the selected property values."""
    class_name = class_dict['name']
    props = []
    for prop in class_dict['repr_return']:
        attr = _lookup_attr(class_dict, prop)
        formatter = '!' if attr['return'] == 'str' else ''
        prop_repr = prop + '={self.' + formatter + prop + '}'
        props.append(prop_repr)
    prop_values = ', '.join(props)
    return_line = f'return (f"<{class_name}Object {prop_values}>")'
    return_wrapped = textwrap.fill(return_line,
                                   width=66,
                                   initial_indent=' ' * 4,
                                   subsequent_indent=' ' * 8)
    if '\n' not in return_wrapped:
        return_wrapped = return_wrapped.replace('(', '').replace(')', '')
    return return_wrapped


def _lookup_attr(class_dict: dict, prop: str) -> dict:
    """Get the attr_dict information from the given prop."""
    for class_attr in class_dict['attrs']:
        if class_attr['name'] == prop:
            return class_attr


def create_property(attr_dict: dict) -> str:
    property_declaration = PROPERTY_TEMPLATE.format(
        attr_name=attr_dict['name'],
        attr_return=attr_dict['return'])
    property_docstring = create_docstring(attr_dict['doc'], 1)
    return_statement = create_property_return_line(attr_dict['return'],
                                                   attr_dict['name'])
    code_text = '\n'.join([property_declaration,
                           property_docstring,
                           return_statement])
    return code_text


def create_property_return_line(return_type: str, attr_name: str) -> str:
    """Create the return line which will instantiate the return type with the
    class's data."""
    return_class, param = _get_return_type_and_params(return_type)

    if return_class == 'datetime':
        return f'return datetime.fromisoformat(self._json_dict[{attr_name!r}])'
    if not param:
        return f'return {return_class}(self._json_dict[{attr_name!r}])'
    if return_class == 'Optional':
        return f'if value := self._json_dict.get({attr_name!r}):\n' \
               f'    return {param}(value)' \
               f'return None'
    if return_class == 'List':
        f'return [{param}(item) for item in self._json_dict[{attr_name!r}]]'
    if return_class == 'Union':
        return f'return union_parser([{param}], self._json_dict[{attr_name!r}])'
    return f'return {return_class}(self._json_dict[{attr_name!r}], {param})'


def _get_return_type_and_params(return_type: str) -> (str, str):
    """Parse the return type and get the class type and any params within
    the brackets of the return_type string."""
    if '[' not in return_type:
        return return_type, None

    bracket_position = return_type.find('[')
    return_class = return_type[:bracket_position]
    param = return_type[bracket_position + 1:-1]
    return return_class, param


def build(directory: str):
    yaml_dicts = create_yaml_dicts('yaml_files')
    class_code = []
    for class_dict in yaml_dicts:
        class_code.append(create_class(class_dict))
    print('\n\n\n'.join(class_code))


build('\\test\\')
