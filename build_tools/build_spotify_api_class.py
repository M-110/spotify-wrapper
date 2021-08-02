"""
Build the Spotify API class
"""
# TODO: Search for an item issues. PagingObject needs to be able to handle
#  multiple possible object types. Right now it just handles 1.
# TODO: Split long urls. yapf isn't splitting them because they're one word.
import os
import textwrap
import re
from typing import List, Union, Optional

import yaml
import yapf

OUTPUT_FILENAME = 'api.py'
YAML_PATH = os.path.join('build_tools', 'yaml_files', 'api_methods.yaml')
BOILERPLATE_PATH = os.path.join('build_tools', 'boilerplate',
                                'spotify_api_class_boiler.py')

METHOD_BODY_TEMPLATE = '''
url = {url}
query_params = {query_params}
json_body = {json_body}
response, error = self._{http_method}(url, query_params, json_body)
if error:
    return ErrorObject(response)
{return_line}
'''


def create_yaml_dicts() -> List[dict]:
    """Open/load the yaml file."""
    with open(YAML_PATH, encoding='utf8') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.Loader)


def create_method_from_yaml_dict(method: dict) -> str:
    """Create the python code for the class method and return it as a
    string."""
    name = method['method_name']
    doc = method['doc']
    http_method = method['http_method']
    endpoint = method['endpoint']
    returns = method['returns']
    scope = method['scope']
    path_parameters = method['path_parameters']
    query_parameters = method['query_parameters']
    json_parameters = method['json_parameters']

    params_dict = create_params_dict(path_parameters,
                                     query_parameters,
                                     json_parameters)

    requires_decorator = create_requires_decorator(scope)
    param_declarations = create_param_declarations(params_dict)
    description_docstring = create_description_docstring(doc)
    params_docstring = create_params_docstring(params_dict)
    docstring = add_triple_quotes_to_docstring(description_docstring +
                                               params_docstring)
    return_line = create_return_line(returns)
    url = format_url(endpoint)

    query_params = create_get_params(params_dict['query_params'])
    json_body = create_get_params(params_dict['json_params'])

    method_declaration = f'def {name}({param_declarations}) -> {returns}:'
    method_body = METHOD_BODY_TEMPLATE.format(url=url,
                                              query_params=query_params,
                                              json_body=json_body,
                                              http_method=http_method,
                                              return_line=return_line)

    method_code = '\n'.join([requires_decorator,
                             method_declaration,
                             textwrap.indent(docstring, ' ' * 4),
                             textwrap.indent(method_body, ' ' * 4)])

    return yapf_format(method_code)


def create_params_dict(path_params: List[Union[str, dict, None]],
                       query_params: List[Union[str, dict, None]],
                       json_params: List[Union[str, dict, None]]) -> dict:
    """Create a dictionary containing all the method's parameters. This is
    mainly for the purpose of flattening the three dictionaries and
    parsing the param values and replacing any preset parameters with a
    corresponding dictionary."""
    params = dict(path_parms=path_params,
                  query_params=query_params,
                  json_params=json_params)
    return {name: parse_param_values(values)
            for name, values in params.items()}


def parse_param_values(values: List[Union[str, dict, None]]
                       ) -> List[Optional[dict]]:
    """Create a list of dictionaries holding the information about each
    parameter. If the value is a string then it is a preset parameter and the
    string must further parsed to create a parameter dictionary."""
    return [create_preset_parameter(value) if isinstance(value, str)
            else value
            for value in values]


def create_preset_parameter(value: str) -> dict:
    """Create a parameter dictionary by parsing the value string and
    constructing a dictionary from it using some preset parameter values.
    
    These are all values that are common through the API methods so this is
    to prevent having to type them out 50+ times in the yaml file. Instead
    shorthand like 'COUNTRY[market]' is used in the yaml file.
    """
    if '[' in value:
        param_name = value[:value.find('[')]
        args = value[value.find('[') + 1:-1].split(',')
    else:
        param_name = value
        args = None

    if param_name == 'COUNTRY':
        doc_string = "An ISO 3166-1 alpha-2 country code or the string " \
                     "'from_token'."
        param_type = 'str'
        param_name = args[0]
        required = bool(args[1:])
    elif param_name == 'LIMIT':
        doc_string = 'The maximum number of {} to return.  Default: {}. ' \
                     'Minimum: {}. Maximum: {}.'.format(*args)
        param_type = 'int'
        required = False
    elif param_name == 'OFFSET':
        doc_string = 'The index of the first {} to return. Default: 0.'.format(
            *args)
        param_type = 'int'
        required = False
    elif param_name == 'ID_':
        doc_string = 'The Spotify ID of the {}.'.format(*args)
        param_type = 'str'
        required = True
    elif param_name == 'LOCALE':
        doc_string = "The desired language, consisting of a lowercase ISO " \
                     "639-1 language code and an uppercase ISO " \
                     "3166-1 alpha-2 country code, joined by an underscore. " \
                     "For example: es_MX, meaning “Spanish (" \
                     "Mexico)”. Provide this parameter if you want the " \
                     "results returned in a particular language (" \
                     "where available). Note that, if locale is not " \
                     "supplied, or if the specified language is not " \
                     "available, all strings will be returned in the " \
                     "Spotify default language (American English). The " \
                     "locale parameter, combined with the country " \
                     "parameter, may give odd results if not carefully " \
                     "matched."
        param_type = 'str'
        required = False
    else:
        raise ValueError(f'{value} not yet implemented.')

    return dict(name=param_name.lower(),
                doc=doc_string,
                required=required,
                type=param_type)


def create_param_declarations(params_dict: dict) -> str:
    """Create the string that will be the method's parameters in the method
    declaration."""
    required_args = []
    optional_args = []

    for params in params_dict.values():
        for param in params:
            if param is None:
                continue
            if param['required']:
                required_args.append(f"{param['name']}: {param['type']}")
            else:
                optional_args.append(
                    f"{param['name']}: {param['type']} = None")

    return ', '.join(['self'] + required_args + optional_args)


def create_description_docstring(doc: str) -> str:
    """Properly format and wrap the description part of the docstring."""
    return textwrap.fill(doc, width=71)


def create_params_docstring(params_dict: dict) -> str:
    """Create the 'Args:' section of the docstring which will list the details
    of what each parameter is."""
    required_args = []
    optional_args = []
    for params in params_dict.values():
        for param in params:
            if param is None:
                continue
            if param['required']:
                required_args.append(
                    create_arg_docstring_line(param))
            else:
                optional_args.append(
                    create_arg_docstring_line(param))
    if not (required_args + optional_args):
        return ''
    else:
        return '\n'.join(['\n\nArgs:'] + required_args + optional_args)


def create_arg_docstring_line(param: dict) -> str:
    """Create a docstring line for the given param."""
    optional = 'Optional; ' if param['required'] else ''
    return textwrap.fill(f"{param['name']}: {optional}{param['doc']}",
                         width=71,
                         initial_indent=' ' * 4,
                         subsequent_indent=' ' * 8)


def add_triple_quotes_to_docstring(docstring: str) -> str:
    """Add triple quotes to surround the docstring."""
    return '"""\n' + docstring + '\n"""'


def create_requires_decorator(scope: List[Optional[str]]) -> str:
    """Create a requirement decorator with the scope that is required to
    make the API call of the method."""
    if scope[0]:
        return ('@requires(' +
                ', '.join([f'{requirement!r}' for requirement in scope]) +
                ')'
                )
    else:
        return ''


def create_return_line(returns: str) -> str:
    """Create the return line for the method which return an instance of the
    corresponding class using json response's text."""
    objects = re.findall(r'\w*Object|bool|str|dict', returns)
    if 'List' in returns:
        return f'return self._convert_array_to_list(response.text, ' \
               f'{objects[0]})'
    elif 'PagingObject' in returns:
        return f'return PagingObject(response.text, {objects[1]})'
    else:
        return f'return {objects[0]}(response.text)'


def format_url(endpoint: str) -> str:
    """Format the  url so that it is does not stretch beyond 65 characters."""
    if len(endpoint) <= 65:
        return endpoint
    elif '{' in endpoint:
        split_point = endpoint.find('{')
    else:
        split_point = len(endpoint) - endpoint[::-1].find('/')
    line_1 = endpoint[:split_point] + "' \\\n"
    line_2 = "      f'" + endpoint[split_point:]
    return line_1 + line_2


def create_get_params(params: List[dict]) -> str:
    """Create the query or json parameters which will be sent in the get
    request."""
    params = [f"{remove_trailing_underscores_from_name(param['name'])!r}: "
              f"{param['name']}"
              for param in params
              if param is not None]

    return '{' + ', '.join(params) + '}'


def remove_trailing_underscores_from_name(name: str):
    """Remove the trailing underscores of variables which shadow built-in
    names such as 'type'."""
    if name.endswith('_'):
        return name[:-1]
    return name


def yapf_format(code: str) -> str:
    """Apply yapf google style formatting to the method's code."""
    config = yapf.style.CreatePEP8Style()
    config['COLUMN_LIMIT'] = 75
    formatted_code = yapf.yapf_api.FormatCode(code, style_config=config)[0]
    return textwrap.indent(formatted_code, ' ' * 4)


def get_boilerplate_code() -> str:
    with open(BOILERPLATE_PATH, 'r', encoding='utf8') as file:
        return file.read()


def write_code_to_file(directory: str,
                       boilerplate_code: str,
                       combined_methods_code: str):
    output_path = os.path.join(directory, OUTPUT_FILENAME)
    with open(output_path, 'w', encoding='utf8') as file:
        file.write(boilerplate_code)
        file.write(combined_methods_code)


def build(directory: str):
    """Parse the yaml file and use it to generate the code for each of the
    methods, combine the method code with the code from the boilerplate file
    and save it as 'api.py' in the given directory."""
    yaml_dicts = create_yaml_dicts()

    code_for_each_method = [create_method_from_yaml_dict(yaml_dict)
                            for yaml_dict in yaml_dicts]
    combined_methods_code = '\n'.join(code_for_each_method)

    boilerplate_code = get_boilerplate_code()

    write_code_to_file(directory, boilerplate_code, combined_methods_code)
