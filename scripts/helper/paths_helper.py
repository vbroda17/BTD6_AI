import os

def create_paths_file(base_dir, output_file="paths.py"):
    """
    Generates a Python script (paths.py) containing uppercase constants for all paths in a directory.

    Args:
        base_dir (str): The base directory to scan for files and folders.
        output_file (str): The name of the output Python file. Default is "paths.py".
    """
    # Open the output file for writing
    with open(output_file, "w") as f:
        # Write the file header
        f.write("# Auto-generated paths file\n")
        f.write("# All paths are defined as uppercase constants\n\n")

        # Traverse the directory and its subdirectories
        for root, dirs, files in os.walk(base_dir):
            # Extract first subfolder for comment
            relative_root = os.path.relpath(root, base_dir)
            first_subfolder = relative_root.split(os.sep)[0].upper() if os.sep in relative_root else None

            # Add comment for the first subfolder
            if first_subfolder and first_subfolder != ".":
                f.write(f"# {first_subfolder}\n")

            # Create a constant name for the current directory
            dir_constant_name = (
                os.path.relpath(root, base_dir)
                .replace(os.sep, "_")
                .upper()
                .replace(".", "_")
            )
            dir_constant_name = f"{dir_constant_name}_DIR" if dir_constant_name != "." else "BASE_DIR"
            dir_path = os.path.relpath(root).replace("\\", "/")
            f.write(f'{dir_constant_name} = "{dir_path}"\n')

            # Create constants for each file in the directory
            for file in files:
                file_constant_name = (
                    f"{dir_constant_name}_{os.path.splitext(file)[0]}"
                    .replace(".", "_")
                    .upper()
                )
                file_path = os.path.relpath(os.path.join(root, file)).replace("\\", "/")
                f.write(f'{file_constant_name} = "{file_path}"\n')

        print(f"Paths file '{output_file}' created successfully.")

if __name__ == "__main__":
    # Hardcoded paths based on provided structure
    base_dir = "images"
    output_file = "scripts/minnor/paths.py"

    create_paths_file(base_dir=base_dir, output_file=output_file)
