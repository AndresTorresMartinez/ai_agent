import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        execution = subprocess.run(["python3", abs_file_path], timeout=30, capture_output=True)
        result = f"STDOUT: {execution.stdout}, STDERR: {execution.stderr}"
        
        if execution.returncode != 0:
            result = result + " Process exited with code X"
        if result is None:
            return "No output produced"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python file from file_path that is inside the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of python file to execute relative to the working directory"
            ),
        },
    ),
)