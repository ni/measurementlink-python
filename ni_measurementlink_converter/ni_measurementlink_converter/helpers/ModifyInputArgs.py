import ast
import astor

def add_parameter_to_method(file_path, method_name, parameter_name):
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            # Add the new parameter as the first parameter in the method's arguments
            new_param = ast.arg(arg=parameter_name, annotation=None)
            node.args.args.insert(0, new_param)

    modified_source = astor.to_source(tree)

    with open(file_path, 'w') as file:
        file.write(modified_source)