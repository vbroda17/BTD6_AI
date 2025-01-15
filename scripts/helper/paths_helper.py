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
            # Extract relative path for comments
            relative_root = os.path.relpath(root, base_dir).replace("\\", "/")
            if relative_root == ".":
                relative_root = ""

            # Generate a hierarchical comment with parent and child folders
            folder_hierarchy = relative_root.replace("/", " - ").upper()
            if folder_hierarchy:
                f.write(f"# {folder_hierarchy}\n")

            # Create constants for each file in the directory
            for file in files:
                if file.endswith('.png'):
                    file_constant_name = (
                        f"{relative_root}/{os.path.splitext(file)[0]}"
                        .replace("/", "_")
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
