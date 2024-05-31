import ast

def insert_session_assigning(file_path, method_name, text_to_insert):
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    # Helper function to find the target method and add text after the with block
    def add_text(node):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            for i, child_node in enumerate(node.body):
                if isinstance(child_node, ast.With):
                    # Get the indentation level of the with statement
                    indent = ' ' * (child_node.col_offset + 4)  # Assuming 4 spaces per level
                    # Construct the text to insert with proper indentation
                    text_line = f'{indent}{text_to_insert}\n'
                    # Insert the text immediately after the with block
                    source_lines = source_code.split('\n')
                    source_lines.insert(child_node.lineno, text_line)
                    # Join the modified source lines
                    modified_source = '\n'.join(source_lines)
                    return modified_source

    modified_source = None
    # Find the target method and add the text
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name == method_name:
                modified_source = add_text(node)
                break

    if modified_source is not None:
        # Write the modified source code to the file
        with open(file_path, 'w') as file:
            file.write(modified_source)
    else:
        print(f"No '{method_name}' method found in the file.")

