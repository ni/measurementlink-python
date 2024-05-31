import pathlib
import ast

def extract_input_details(file_path, method_name):
    # Parse the Python file to extract the AST
    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)
    
    # Find the method node in the AST
    method_node = next((node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == method_name), None)
    if method_node is None:
        print(f"Method '{method_name}' not found in the file.")
        return {}
    
    # Analyze types of default values for parameters
    parameter_types = {}
    defaults = method_node.args.defaults or []
    args_without_defaults = method_node.args.args[:len(method_node.args.args) - len(defaults)]
    
    for arg in args_without_defaults:
        param_name = arg.arg
        param_type = None
        
        # Extract parameter type from annotation
        if arg.annotation:
            if isinstance(arg.annotation, ast.Name):
                param_type = arg.annotation.id  # Simple type like int, str, etc.
            elif isinstance(arg.annotation, ast.Subscript):
                if isinstance(arg.annotation.value, ast.Name):
                    param_type = arg.annotation.value.id
                    if isinstance(arg.annotation.slice, ast.Name):
                        param_type += f"[{arg.annotation.slice.id}]"
        
        # Assign default value based on parameter type if it's not provided
        default_value = None
        if param_type == 'int':
            default_value = 0
        elif param_type == 'str':
            default_value = ''
        
        # Store parameter name, type, and default value
        parameter_types[param_name] = {"type": param_type, "default": default_value}
    
    # Assign default values for the remaining parameters
    for arg, default_node in zip(method_node.args.args[len(args_without_defaults):], defaults):
        param_name = arg.arg
        param_type = None
        
        # Extract parameter type from annotation
        if arg.annotation:
            if isinstance(arg.annotation, ast.Name):
                param_type = arg.annotation.id  # Simple type like int, str, etc.
            elif isinstance(arg.annotation, ast.Subscript):
                if isinstance(arg.annotation.value, ast.Name):
                    param_type = arg.annotation.value.id
                    if isinstance(arg.annotation.slice, ast.Name):
                        param_type += f"[{arg.annotation.slice.id}]"
        
        # Extract default value
        default_value = ast.literal_eval(default_node)
        
        # Store parameter name, type, and default value
        parameter_types[param_name] = {"type": param_type, "default": default_value}
    
    return parameter_types
