import yaml
import textwrap

# TODO: Image upload?

header_template = '''{requires_decorator}
def {method_name}({params}) -> {return_type}:
    """
{method_doc}
    """
    url = {url}
    query_params = {query_params}
    json_body = {json_body}
    response = self._{http_method}(url, query_params, json_body)
'''

args_docstring_template = '''
Args:
{args}
'''

prop_template = '''
    @property
    def {attr_name}(self) -> {attr_return}:
        """
{attr_doc}
        """
        return self._json_dict['{attr_name}']
'''


def generate_preset_param(param: str) -> dict:
    if '[' in param:
        param_name = param[:param.find('[')]
        args = param[param.find('[') + 1:-1].split(',')
    else:
        param_name = param
        args = None

    if param_name == 'COUNTRY':
        doc_string = "An ISO 3166-1 alpha-2 country code or the string 'from_token'."
        param_type = 'str'
        param_name = args[0]
        required = bool(args[1:])
    elif param_name == 'LIMIT':
        doc_string = 'The maximum number of {} to return.  Default: {}. Minimum: {}. Maximum: {}.'.format(*args)
        param_type = 'int'
        required = False
    elif param_name == 'OFFSET':
        doc_string = 'The index of the first {} to return. Default: 0.'.format(*args)
        param_type = 'int'
        required = False
    elif param_name == 'ID_':
        doc_string = 'The Spotify ID of the {}.'.format(*args)
        param_type = 'str'
        required = True
    elif param_name == 'LOCALE':
        doc_string = "The desired language, consisting of a lowercase ISO 639-1 language code and an uppercase ISO " \
                     "3166-1 alpha-2 country code, joined by an underscore. For example: es_MX, meaning “Spanish (" \
                     "Mexico)”. Provide this parameter if you want the results returned in a particular language (" \
                     "where available). Note that, if locale is not supplied, or if the specified language is not " \
                     "available, all strings will be returned in the Spotify default language (American English). The " \
                     "locale parameter, combined with the country parameter, may give odd results if not carefully " \
                     "matched."
        param_type = 'str'
        required = False
    else:
        raise ValueError(f'{param} not yet implemented.')

    return dict(name=param_name.lower(),
                doc=doc_string,
                required=required,
                type=param_type)


def generate_param_dict(path_params, query_params, json_params) -> dict:
    """Create a dictionary of all the method's parameters."""
    params = dict(path_params=path_params,
                  query_params=query_params,
                  json_params=json_params)
    return {param_name: [generate_preset_param(param)
                         if isinstance(param, str)
                         else param
                         for param in param_values]
            for param_name, param_values in params.items()}


def generate_param_declarations(param_dict: dict) -> str:
    """Returns a string to be used as the method's arguments."""
    required_args = []
    optional_args = []
    for params in param_dict.values():
        for param in params:
            if param is None:
                continue
            if param['required']:
                required_args.append(f"{param['name']}: {param['type']}")
            else:
                optional_args.append(f"{param['name']}: {param['type']} = None")

    return ', '.join(['self'] + required_args + optional_args)


def generate_params_docstring(param_dict: dict) -> str:
    """Create the Args docstring to be inserted into the method's docstring."""
    required_args = []
    optional_args = []
    for params in param_dict.values():
        for param in params:
            if param is None:
                continue
            if param['required']:
                required_args.append(
                    textwrap.fill(f"{param['name']}: {param['doc']}",
                                  width=78,
                                  initial_indent=' ' * 8,
                                  subsequent_indent=' ' * 10))
            else:
                optional_args.append(
                    textwrap.fill(f"{param['name']}: Optional; {param['doc']}",
                                  width=78,
                                  initial_indent=' ' * 8,
                                  subsequent_indent=' ' * 10))
    if not (required_args + optional_args):
        return ''
    else:
        return '\n'.join(['\n\n    Args:'] + required_args + optional_args)


def generate_requires_decorator(scope: list) -> str:
    """Returns a string that adds the necessary scope requirements to the requires
    decorator, or an empty string if there is no scope."""
    if scope[0]:
        return '\n@requires(' + ', '.join([f'{s!r}' for s in scope]) + ')'
    else:
        return ''


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


def yaml_to_class(filename):
    with open(filename, 'r', encoding='utf-8') as yaml_file:
        yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)

    output = ''

    for class_ in yaml_dict:
        header = header_template.format(class_name=class_['name'],
                                        class_doc=class_wrap(class_['doc']))
        output += header
        for attr in class_['attrs']:
            prop = prop_template.format(attr_name=attr['name'],
                                        attr_doc=attr_wrap(attr['doc']),
                                        attr_return=attr['return'])
            output += prop
        output += '\n'

    return output


def parse_yaml_method(method: dict):
    name = method['method_name']
    doc = method['doc']
    http_method = method['http_method']
    endpoint = method['endpoint']
    returns = method['returns']
    scope = method['scope']

    params_dict = generate_param_dict(method['path_parameters'],
                                      method['query_parameters'],
                                      method['json_parameters'])
    param_declarations = generate_param_declarations(params_dict)
    params_docstring = generate_params_docstring(params_dict)
    requires_decorator = generate_requires_decorator(scope)
    url = endpoint

    query_params = '{' + ', '.join([f"{param['name']!r}: {param['name']}"
                                    for param in params_dict['query_params']
                                    if param is not None]) + '}'
    json_body = '{' + ', '.join([f"{param['name']!r}: {param['name']}"
                                 for param in params_dict['json_params']
                                 if param is not None]) + '}'
    output = header_template.format(requires_decorator=requires_decorator,
                                    method_name=name,
                                    params=param_declarations,
                                    return_type=returns,
                                    method_doc=class_wrap(doc) + params_docstring,
                                    url=url,
                                    query_params=query_params,
                                    json_body=json_body,
                                    http_method=http_method)
    return output


def yaml_to_methods(filename):
    with open(filename, 'r', encoding='utf-8') as yaml_file:
        yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)

    output = ''

    for method in yaml_dict:
        print(parse_yaml_method(method))
    return output


if __name__ == "__main__":
    class_output = yaml_to_methods('methods.yaml')
    print(class_output)
