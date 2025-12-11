"""Project builder CLI and helpers.

This module reads a YAML-based project specification and creates the
directory and file skeleton described by that spec. It's intentionally
small and opinionated — it expects a YAML structure with a top-level
`project` mapping and a `directories` sequence describing nested
directories and files.

Expected YAML structure example:

project:
    name: my_project
    version: 0.1
    description: Example project

directories:
    - name: src
        type: directory
        children:
            - name: models
                type: directory
            - name: __init__.py
                type: file

Usage:
    - As a script: `python project_builder.py project_structure.yaml`
    - As an import: call `main(path_to_yaml)`

The script walks `directories` as a stack, expanding `children` by
concatenating paths (so child names become `parent/child`) and then
creates directories or files as specified.

Note: This module performs filesystem side-effects (creating folders
and writing minimal stub files). Use with caution in directories with
important data.
"""

import os
import sys
from typing import List

import yaml


def read_yaml_file(file_path: str):
    """Load and parse a YAML file.

    Parameters
    - file_path: Path to a YAML file containing the project spec.

    Returns
    - Parsed Python object (usually a dict) on success, or `None` on
      failure. Failures include file not found or YAML parse errors.

    The function uses `yaml.safe_load` to avoid executing arbitrary
    constructors from YAML content.
    """
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
    """Create a directory (including parents) if it doesn't exist.

    Parameters
    - directory_path: Path to create. May be relative (e.g. `./src`) or
        absolute. The function will create intermediate directories as
        needed.

    Behavior
    - Checks if the directory already exists. If it does, prints a message
      and aborts the operation.
    - Otherwise, creates the directory and all intermediate parents.
    """
    # Create the directory
    if os.path.isdir(directory_path):
        print(f"directory {directory_path} exists. operation aborted.")
    else:
        os.makedirs(directory_path, exist_ok=False)
        print(f"created directory {directory_path}.")


def create_empty_file(file_path: str):
    """Create a simple placeholder file.

    Parameters
    - file_path: Path of the file to create. If parent directories do not
      exist this function will raise.

    Behavior
    - Checks if the file already exists. If it does, prints a message and
      aborts the operation.
    - Otherwise, creates the file with a single-line comment to indicate
      it was generated.
    """

    if os.path.isfile(file_path):
        print(f"file {file_path} exists. operation aborted.")
    else:
        with open(file_path, "w") as f:
            f.write("# file automatically generated")
        print(f"Created file ./{file_path}")


def setup_logging(log_file_path: str, root_log_level: str):
    """Generate and write a logging configuration file.

    Parameters
    - log_file_path: Path where logs should be written.
    - root_log_level: Root logging level (e.g., 'DEBUG', 'INFO', 'WARNING').

    Behavior
    - Reads a template from `logging_config_template.json`.
    - Replaces placeholders `${LOG_FILE_PATH}` and `${ROOT_LOG_LEVEL}` with
      provided values.
    - Writes the templated content to `configs/logging/logging_config.json`
      if the `configs/logging` directory exists.
    - Prints a confirmation message on success.
    """

    # Read the template file content
    with open("logging_config_template.json", "r") as f:
        template_content = f.read()

    # Replace placeholders with actual values
    # You could also use a loop or dict for many variables
    templated_content = template_content.replace("${LOG_FILE_PATH}", log_file_path)
    templated_content = templated_content.replace(
        "${ROOT_LOG_LEVEL}", root_log_level
    )  # noqa: E501

    # if logging directory exists
    logging_dir: str = "configs/logging"
    logging_config_name: str = "logging_config.json"
    if os.path.isdir("configs/logging"):
        with open(os.path.join(logging_dir, logging_config_name), "w") as f:
            f.write(templated_content)

        print(
            f"logging configuration saved at {os.path.join(
                logging_dir, logging_config_name
            )}"
        )


def main(file_path: str):
    """Build a project skeleton and logging configuration from YAML.

    Parameters
    - file_path: Path to the YAML configuration file to read.

    Behavior
    - Reads the YAML via `read_yaml_file`.
    - Prints basic project metadata (`project.name`, `project.version`,
      `project.description`) if present.
    - Walks entries in `directories`. Each item must have a `name` and
      a `type` of either `'directory'` or `'file'`. If an item has a
      `children` list, children names are joined to the parent path
      (e.g. parent `src` and child `models` become `src/models`) and
      re-inserted into the processing stack.
    - Reads `logging.root_log_level` and `logging.log_file_path` from the
      YAML config and calls `setup_logging` to generate the logging
      configuration.

    Side effects: creates directories and files on disk using
    `create_directory` and `create_empty_file`, and writes a logging
    configuration file via `setup_logging`.
    """

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
                create_empty_file(directory["name"])

        root_log_level: str = config["logging"]["root_log_level"]
        log_file_path: str = config["logging"]["log_file_path"]

        setup_logging(log_file_path=log_file_path, root_log_level=root_log_level)


if __name__ == "__main__":
    print(f"Script name: {sys.argv[0]}")

    if len(sys.argv) > 1:
        filename: str = sys.argv[1]
        print(f"Filename: {filename}")
    else:
        print("No arguments provided.")

    main(filename)
