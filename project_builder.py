import os
import sys
from typing import List

import yaml


def read_yaml_file(file_path: str):
    """Reads a YAML file and returns a Python dictionary."""
    try:
        with open(file_path, "r") as file:
            # Use safe_load to safely parse the YAML file
            config_data = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None


def create_directory(directory_path: str):
    # Create the directory
    os.makedirs(directory_path, exist_ok=True)
    print(f"created directory ./{directory_path}")


def create_file(file_path: str):
    with open(file_path, "w") as f:
        f.write("# file generated automatically")
    print(f"Created file ./{file_path}")


def main(file_path: str):

    # --- Main execution ---
    config = read_yaml_file(file_path)

    if config:
        print("Successfully loaded configuration:")
        print("-" * 30)

        print(f"Project name: {config['project']['name']}")
        print(f"Project version: {config['project']['version']}")
        print(f"Project description: {config['project']['description']}")

        directories: List[str, any] = config["directories"]

        while len(directories) > 0:
            directory = directories.pop()
            name = directory["name"]
            if "children" in directory:
                sub_directories = directory["children"]
                for d in sub_directories:
                    sub_name = d["name"]
                    d["name"] = f"{name}/{sub_name}"
                    directories.append(d)

            if directory["type"] == "directory":
                create_directory(f"./{directory['name']}")
            elif directory["type"] == "file":
                create_file(directory["name"])


if __name__ == "__main__":
    print(f"Script name: {sys.argv[0]}")

    if len(sys.argv) > 1:
        filename: str = sys.argv[1]
        print(f"Filename: {filename}")
    else:
        print("No arguments provided.")

    main(filename)
