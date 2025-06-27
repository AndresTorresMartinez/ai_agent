import os
from google.genai import types
MAX_CHARS = 10000

def file_path_check(directory, file_path):
    if "/" not in file_path:
        if file_path not in os.listdir(directory) and file_path != ".":
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        return
    folders = file_path.split("/")
    file_path_check(os.path.join(directory, folders[0]), "/".join(folders[1:]))

def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        
        file_path_check(working_directory, file_path)       
        
        full_dir = os.path.join(working_directory, file_path)
        
        if not os.path.isfile(full_dir):
            f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(full_dir) > MAX_CHARS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        
        return file_content_string
    except Exception as e:
        return f"Error: R {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the content of the specified file in file_path that is inside working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read relative to the working directory"
            ),
        },
    ),
)