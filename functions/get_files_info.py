import os

def get_files_info(working_directory, directory=None):
    try:
        working_directory = os.path.abspath(working_directory)
        
        if directory not in os.listdir(working_directory) and directory != ".":
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        full_dir = os.path.join(working_directory, directory)
        
        if not os.path.isdir(full_dir):
            return f'Error: "{full_dir}" is not a directory'
        
        def print_metadata(file):
            full_path = os.path.join(full_dir, file)
            return f"- {full_path}: file_size={os.path.getsize(full_path)} is_dir={os.path.isdir(full_path)}"
        
        return "\n".join(list(map(print_metadata, os.listdir(full_dir))))
    except Exception as e:
        return f"Error: {e}"