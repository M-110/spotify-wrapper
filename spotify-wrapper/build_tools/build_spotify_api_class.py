"""
Build the Spotify API class
"""
import os
import textwrap
from typing import List, Dict, Union, Optional

import yaml

YAML_PATH = os.path.join('yaml_files', 'api_methods.yaml')
BOILERPLATE_PATH = os.path.join('boilerplate', 'spotify_api_class_boiler.py')


def create_yaml_dicts() -> List[dict]:
    """Open/load the yaml file."""
    with open(YAML_PATH, encoding='utf8') as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.Loader)


def create_method(method: dict) -> str:
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
    param_declarations = create_param_declarations(params_dict)
    params_docstring = create_params_docstring(params_dict)
    requires_decorator = create_requires_decorator(scope)
    return_line = create_return_line(returns)
    url = endpoint
    
    query_params = '?'
    json_body = '?'
    
    output = '?'
    
    return output


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
                optional_args.append(f"{param['name']}: {param['type']} = None")

    return ', '.join(['self'] + required_args + optional_args)


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
        return '\n'.join(['\n\n    Args:'] + required_args + optional_args)


def create_arg_docstring_line(param: dict) -> str:
    """Create a docstring line for the given param."""
    optional = 'Optional; ' if param['required'] else ''
    return textwrap.fill(f"{param['name']}: {optional}{param['doc']}",
                         width=78,
                         initial_indent=' ' * 8,
                         subsequent_indent=' ' * 12)


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
    

def create_return_line(returns: str):
    """."""


def build(directory: str):
    output_path = os.path.join(directory, 'api.py')
    with open(BOILERPLATE_PATH, 'r', encoding='utf8') as file:
        boiler = file.read()

    yaml_dicts = create_yaml_dicts()
    method_code = [create_method(method_dict) for method_dict in yaml_dicts]
    all_methods = '\n\n'.join(method_code)

    with open(output_path, 'w', encoding='utf8') as file:
        file.write(boiler)
        file.write(all_methods)
        file.write('\n')
