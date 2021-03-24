import yaml
import textwrap

header_template = '''
{requires_decorator}
def {method_name}(self, {params}) -> {return_type}:
    """
{method_doc}
    """
    
    
    response = self._{http_method}(url)
'''

prop_template = '''
    @property
    def {attr_name}(self) -> {attr_return}:
        """
{attr_doc}
        """
        return self._json_dict['{attr_name}']
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
    scope = method['header']['scope']
    content_type = method['header']['content_type']
    
    path_params = method['path_parameters']
    
    query_params = method['query_parameters']
    
    json_params = method['json_parameters']
    
    if scope[0]:
        requires_decorator = '\n@requires(' + ', '.join([f'{s!r}' for s in scope]) + ')'
    else:
        requires_decorator = ''
        
    output = header_template.format(requires_decorator=requires_decorator,
                                    method_name=name,
                                    params=str(path_params),
                                    return_type=returns,
                                    method_doc=doc,
                                    http_method=http_method,
                                    url=endpoint)
    return output
    

        
    
    


def yaml_to_methods(filename):
    with open(filename, 'r', encoding='utf-8') as yaml_file:
        yaml_dict = yaml.load(yaml_file, Loader=yaml.Loader)

    output = ''

    for method in yaml_dict:
        print(parse_yaml_method(method))
    return output

class_output = yaml_to_methods('methods_2.yaml')
print(class_output)
