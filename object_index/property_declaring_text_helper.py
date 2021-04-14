import yaml
import textwrap

header_template = '''
class {class_name}Object(SpotifyObject):
    """
{class_doc}
    """
'''

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



def yaml_to_class(filename):
    with open(filename, 'r', encoding='utf-8') as yaml_file:
        yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)

    output = ''

    for class_ in yaml_dict:
        header = header_template.format(class_name=class_['name'],
                                        class_doc=class_wrap(class_['doc']))
        output += header
        for attr in class_['attrs']:
            return_statement = parse_return_type(attr['return'], attr['name'])
            prop = prop_template.format(attr_name=attr['name'],
                                        attr_doc=attr_wrap(attr['doc']),
                                        attr_return=attr['return'],
                                        return_statement=return_statement)
            output += prop
        output += '\n'

    return output


def main():
    class_output = yaml_to_class('objects.yaml')
    with open('boiler_plate.py', encoding='utf-8') as boiler:
        with open('object_library.py', 'w', encoding='utf8') as lib:
            lib.writelines(boiler)
            lib.write(class_output)
    print('Saved as \'object_library.py\'')


if __name__ == "__main__":
    main()
