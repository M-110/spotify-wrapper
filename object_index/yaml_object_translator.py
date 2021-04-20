from typing import List

import yaml
import textwrap

header_template = '''
class {class_name}Object(SpotifyObject):
    """
{class_doc}
    """
'''

repr_template = """
    def __repr__(self):
{repr_return}
"""

prop_template = '''
    @property
    def {attr_name}(self) -> {attr_return}:
        """
{attr_doc}
        """
        {return_statement}
'''


def class_wrap(class_text: str):
    return '\n'.join(
        textwrap.fill(line,
                      width=78,
                      initial_indent=' ' * 4,
                      subsequent_indent=' ' * (4 + len(line) - len(line.strip())))
        for line in class_text.splitlines())


def attr_wrap(attr_text: str):
    return '\n'.join(
        textwrap.fill(line,
                      width=78,
                      initial_indent=' ' * 8,
                      subsequent_indent=' ' * (8 + len(line) - len(line.strip())))
        for line in attr_text.splitlines())


def parse_return_type(return_type: str, attr_name: str):
    if '[' in return_type:
        return_class = return_type[:return_type.find('[')]
        param = return_type[return_type.find('[') + 1:-1]
    else:
        return_class = return_type
        param = None

    if return_class == 'datetime':
        return f'return datetime.fromisoformat(self._json_dict[{attr_name!r}])'
    elif not param:
        return f'return {return_class}(self._json_dict[{attr_name!r}])'
    elif return_class == "Optional":
        return generate_optional_return(param, attr_name)
    elif return_class == "List":
        return f'return [{param}(item) for item in self._json_dict[{attr_name!r}]]'
    if return_class == "Union":
        return f"return union_parser([{param}], self._json_dict[{attr_name!r}])"
    else:
        return f'return {return_class}(self._json_dict[{attr_name!r}], {param})'


def generate_optional_return(target_class, attr_name):
    if target_class == "datetime":
        target_class = "datetime.fromisoformat"
    return f"""if value := self._json_dict.get({attr_name!r}):
            return {target_class}(value)
        return None"""


def lookup_attr(class_: dict, attr: str) -> dict:
    for class_attr in class_['attrs']:
        if class_attr['name'] == attr:
            return class_attr


def generate_repr_return(class_: dict) -> str:
    class_name = class_['name']
    props = []
    for prop in class_['repr_return']:
        prop_repr = prop + "={self." + prop
        attr = lookup_attr(class_, prop)
        if attr['return'] == 'str':
            prop_repr += "!r"
        prop_repr += "}"
        props.append(prop_repr)
    return_line = f"return (f'<{class_name}Object {', '.join(props)}>')"
    return_wrapped = textwrap.fill(return_line,
                                   width=78,
                                   initial_indent=' ' * 8,
                                   subsequent_indent=' ' * 16,
                                   drop_whitespace=False,
                                   ).replace('\n                ', '\'\n                f\'')
    # If one line, remove redundant parentheses
    if '\n' not in return_wrapped:
        return_wrapped = return_wrapped.replace('(', '').replace(')', '')
    return return_wrapped


def yaml_to_class(filename):
    with open(filename, 'r', encoding='utf-8') as yaml_file:
        yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)

    output = ''

    for class_ in yaml_dict:
        header = header_template.format(class_name=class_['name'],
                                        class_doc=class_wrap(class_['doc']))

        repr_return = generate_repr_return(class_)

        repr_method = repr_template.format(repr_return=repr_return)
        output += header + repr_method
        for attr in class_['attrs']:
            return_statement = parse_return_type(attr['return'], attr['name'])
            prop = prop_template.format(attr_name=attr['name'],
                                        attr_doc=attr_wrap(attr['doc']),
                                        attr_return=attr['return'],
                                        return_statement=return_statement)
            output += prop
        output += '\n'

    return output


def translate_yaml_to_classes(file_out: str):
    class_output = yaml_to_class('objects.yaml')
    with open('object_library_boiler_plate.py', encoding='utf-8') as boiler:
        with open(file_out, 'w', encoding='utf8') as lib:
            lib.writelines(boiler)
            lib.write(class_output)
    print(f'Saved as {file_out!r}')


if __name__ == "__main__":
    translate_yaml_to_classes('..\\spotify_wrapper\\object_library.py')
