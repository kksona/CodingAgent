import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        # 1. Path Security & Validation
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        # Check if target is within permitted working directory
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 2. Check if the path is actually a regular file
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # 3. Read content with truncation check
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            # Try to read one more character to check for truncation
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return content

    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a specific file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)