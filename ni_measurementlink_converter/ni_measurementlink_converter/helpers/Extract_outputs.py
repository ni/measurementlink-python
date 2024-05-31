import ast
from typing import Tuple, List, Any


def extract_type(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Subscript):
        generic_type = extract_type(node.value)
        if isinstance(node.slice, ast.Tuple):
            inner_types = [extract_type(elt) for elt in node.slice.elts]
            return inner_types
        elif isinstance(node.slice, ast.Index):
            slice_id = extract_type(node.slice.value)
            return f'{generic_type}[{slice_id}]'
        else:
            slice_id = extract_type(node.slice)
            return f'{generic_type}[{slice_id}]'
    else:
        return ""

def get_return_details(file_path: str, method_name: str) -> Tuple[List[str], List[Any]]:
    with open(file_path, 'r') as file:
        source_code = file.read()

    # Parse the source code to find the method
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            method_node = node
            break
    else:
        raise ValueError(f"Method '{method_name}' not found in file '{file_path}'")

    # Extract return type annotation from method node
    return_type_annotation = method_node.returns

    # Extract the return type
    return_type = extract_type(return_type_annotation)

    # Parse the method's source code to find variables in the return statement
    method_source = ast.get_source_segment(source_code, method_node)
    method_tree = ast.parse(method_source)
    return_variables = []
    for node in ast.walk(method_tree):
        if isinstance(node, ast.Return):
            if isinstance(node.value, ast.Tuple):  # Check if return value is a tuple
                for element in node.value.elts:
                    return_variables.extend(extract_list_types(element))
            elif isinstance(node.value, ast.Name):
                return_variables.append(node.value.id)

    return return_variables, return_type

def extract_list_types(node):
    if isinstance(node, ast.Name):
        return [node.id]
    elif isinstance(node, ast.List):
        inner_types = [extract_type(elt) for elt in node.elts]
        return inner_types
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "List":
        return [extract_type(arg) for arg in node.args]
    else:
        return []

def flatten_list(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(item)
        else:
            flat_list.append(item)
    return flat_list
