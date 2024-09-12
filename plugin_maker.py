import os
import zipfile
import json

def zip_directory(directory_path, output_zip_path):
    """
    Zips the given directory and saves it to the output zip path.

    Args:
        directory_path (str): The path to the directory to be zipped.
        output_zip_path (str): The path where the output zip file will be saved.
    """
    # Check for the manifest file
    manifest_path = os.path.join(directory_path, 'manifest.json')
    if not os.path.exists(manifest_path):
        print(f"Warning: No manifest.json file found in {directory_path}. The directory will not be zipped.")
        return
    
    # Validate the manifest file
    if not validate_manifest(manifest_path):
        print(f"Error: Invalid manifest.json file in {directory_path}. The directory will not be zipped.")
        return

    # Create a zip file
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through the directory structure
        for folder_name, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                # Create the complete file path
                file_path = os.path.join(folder_name, filename)
                # Add file to zip archive
                zip_file.write(file_path, os.path.relpath(file_path, directory_path))
    print(f"Directory '{directory_path}' has been zipped to '{output_zip_path}'.")

def validate_manifest(manifest_path):
    """
    Validates the manifest file to ensure it has the necessary fields.

    Args:
        manifest_path (str): The path to the manifest file.

    Returns:
        bool: True if the manifest is valid, False otherwise.
    """
    try:
        with open(manifest_path, 'r') as file:
            manifest = json.load(file)
        required_fields = ["name", "version", "game_version", "python_version"]

        # Check for the presence of required fields
        for field in required_fields:
            if field not in manifest:
                print(f"Manifest is missing required field: {field}")
                return False

        return True

    except json.JSONDecodeError:
        print(f"Error: Unable to parse manifest file '{manifest_path}'.")
        return False

def check_directory_structure(directory_path):
    """
    Prints the structure of the given directory.

    Args:
        directory_path (str): The path to the directory whose structure is to be printed.
    """
    print(f"Checking structure of directory: {directory_path}")
    for folder_name, subfolders, filenames in os.walk(directory_path):
        print(f"Directory: {folder_name}")
        for subfolder in subfolders:
            print(f"  Subdirectory: {subfolder}")
        for filename in filenames:
            print(f"  File: {filename}")

# Example Usage
directory_to_zip = 'plugins/probability_playground'  # Path to the directory you want to zip
output_zip_file = 'game_visualizer_plugin.zip'  # Name of the output zip file

# Check the directory structure
check_directory_structure(directory_to_zip)

# Zip the directory if manifest is valid
zip_directory(directory_to_zip, output_zip_file)
