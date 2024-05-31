
import ast
import astor

def replace_session_initialization(file_path, method_name, driver_names):
    replacements = []
    with open(file_path, 'r') as file:
        source_code = file.read()
    tree = ast.parse(source_code)
    # Helper function to replace session initialization
    def replace_session(node, driver_name):
        if isinstance(node, ast.With):
            if hasattr(node, 'items') and node.items:
                for item in node.items:
                    if isinstance(item.context_expr, ast.Call):
                        call = item.context_expr
                        if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name):
                            if call.func.value.id == driver_name and call.func.attr == 'Session':
                                actual_session_name = item.optional_vars.id
                                item.optional_vars.id = 'session_info'
                                call.func.attr = f'initialize_{driver_name}_session'
                                call.func.value.id = 'reservation'
                                replacements.append((driver_name, call.keywords[0].value.s, actual_session_name))
                                call.keywords.clear()
    # Traverse the AST to find the method and replace session initialization
    method_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            method_found = True
            for driver_name in driver_names:
                for child_node in ast.walk(node):
                    replace_session(child_node, driver_name)
    if not method_found:
        print(f"Method '{method_name}' not found in the file.")
    modified_source = astor.to_source(tree)
    with open(file_path, 'w') as file:
        file.write(modified_source)
    return replacements
