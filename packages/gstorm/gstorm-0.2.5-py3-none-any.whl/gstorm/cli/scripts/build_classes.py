import os
import click
from .utils import one_to_one_map, imports, example
from gstorm.helpers.gql_schema_helpers import load_schema_from_file
from ValiotWorker.Logging import log, LogLevel

def _build_classes(schema, dir_to_save, mpath):

    for class_name, attributes in schema.items():
        path_and_file = os.path.join(dir_to_save, class_name + ".py")
        log(LogLevel.WARNING, f'Building class file for {class_name} model')
        with open(path_and_file, 'w') as file:

            # * Clases GraphQLType
            if attributes['kind'] == 'TYPE':
                file.write( imports ) 
                buffer_written = f"\nmpath = '{mpath}'\n\n@attr.s\nclass {class_name}(GraphQLType):\n"

                for field in attributes['fields']:
                    name = field['name']
                    kind = field['type']['kind']
                    temp = field['type']['name']
                    has_one = field['has_one']
                    unique = field['unique']
                    if any([unique, has_one]):
                        metadata = ", metadata={{{0}{1}{2}}}"\
                        .format("'unique':{}" if unique else '', \
                            ',' if all([has_one, unique]) else '', \
                            "'has_one':True" if has_one else '')
                    else: metadata = ''
                    type_name, default = (temp,"None") if temp not in one_to_one_map else one_to_one_map[temp]
                            
                    if kind == "OBJECT":
                        buffer_written += \
                            f"    {name}: GraphQLType = attr.ib(default={default}, repr=gql_repr, converter=convert_to(mpath,'{type_name}') {metadata})\n"
                    elif kind == "LIST":
                        buffer_written += \
                            f"    {name}: List[GraphQLType] = attr.ib(factory=list, repr=gql_list_repr, converter=list_convert_to(mpath,'{type_name}'), metadata={{'type':list}})\n"
                    elif kind == "ENUM":
                        file.write(f"from .{type_name} import {type_name}\n")
                        buffer_written += \
                            f"    {name}: {type_name} = attr.ib(default='{schema[type_name]['enumValues'][0]}', converter=convert_to(mpath,'{type_name}'){metadata})\n"
                    else:
                        buffer_written += \
                            f"    {name}: {type_name} = attr.ib(default={default}{metadata})\n"

            # * Clases Enum
            elif attributes['kind'] == 'ENUM':
                file.write("from enum import Enum")
                buffer_written = f"\n\nclass {class_name}(Enum):\n"     
                for enum in attributes['enumValues']:
                    buffer_written += f"    {enum} = '{enum}'\n"
            
            file.write(buffer_written)

    # Creacion del archivo __init__.py
    path_and_file = os.path.join(dir_to_save, "__init__.py")
    with open(path_and_file, 'w') as file:
        for class_name in schema:
            file.write(f"from .{class_name} import {class_name}\n")
            

@click.command()
@click.option('--src', default=None, help='Graphql schema file to analyze')
@click.option('--output', default=None, help='output directory for the GQL model files')
def build_classes(src, output):
    mpath = output.replace('/', '.')
    output = os.path.join(os.getcwd(), output)
    schema = load_schema_from_file(src)
    _build_classes(schema, output, mpath)
    log(LogLevel.SUCCESS, 'Done')
