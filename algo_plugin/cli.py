import os
import json
import zipfile
import argparse

def create_plugin_structure():
    print("Welcome to the Plugin Creator!")
    
    plugin_name = input("Enter the plugin name: ")
    game_version = input("Enter the game version compatible with the plugin: ")
    python_version = input("Enter the minimum Python version required: ")
    dependencies = input("Enter a comma-separated list of dependencies (e.g., pygame,numpy): ").split(',')
    author = input("Enter the author of the plugin: ")
    contact = input("Enter the contact information of the author: ")
    
    plugin_dir = f'plugins/{plugin_name}'
    assets_dir = os.path.join(plugin_dir, 'assets')
    
    os.makedirs(assets_dir, exist_ok=True)
    
    manifest_content = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": f"A plugin for {plugin_name}.",
        "game_version": game_version,
        "python_version": python_version,
        "dependencies": [dep.strip() for dep in dependencies],
        "author": author,
        "contact": contact
    }
    
    manifest_path = os.path.join(plugin_dir, 'manifest.json')
    init_path = os.path.join(plugin_dir, '__init__.py')
    plugin_path = os.path.join(plugin_dir, 'plugin.py')
    requirements_path = os.path.join(plugin_dir, 'requirements.txt')
    base_path = os.path.join(plugin_dir, 'plugin_base.py')
    
    # Create manifest.json
    with open(manifest_path, 'w') as file:
        json.dump(manifest_content, file, indent=4)
    
    # Create __init__.py
    with open(init_path, 'w') as file:
        file.write('')
    
    # Create plugin_base.py
    with open(base_path, 'w') as file:
        file.write('''
class PluginBase:
    def __init__(self, plugin_id):
        """
        Initialize the plugin. Set up any necessary variables, load resources, etc.
        :param plugin_id: Unique identifier for the plugin.
        """
        self.plugin_id = plugin_id  # Unique ID for the plugin
        self.active = True  # Control whether the plugin is active or not

    def update(self, events, delta_time):
        """
        Update the game logic. This will be called by the main loop.
        :param events: List of Pygame events.
        :param delta_time: Time elapsed since the last frame (to make movements frame rate independent).
        """
        raise NotImplementedError("The 'update' method must be implemented by the plugin.")

    def draw(self, surface):
        """
        Draw the plugin content on the provided Pygame surface.
        :param surface: Pygame surface where the plugin should render its output.
        """
        raise NotImplementedError("The 'draw' method must be implemented by the plugin.")
        ''')
    
    # Create plugin.py
    with open(plugin_path, 'w') as file:
        file.write(f'''
from plugin_base import PluginBase

class {plugin_name}Plugin(PluginBase):
    def __init__(self, screen):
        super().__init__(plugin_id="your_unique_plugin_id")
        self.screen = screen

    def update(self, events, delta_time):
        # Implement your plugin's update logic here
        pass

    def draw(self, surface):
        # Implement your plugin's drawing logic here
        pass
        ''')

    # Create requirements.txt
    with open(requirements_path, 'w') as file:
        for dependency in manifest_content['dependencies']:
            file.write(f'{dependency}\n')
    
    print(f"Plugin structure created at: {plugin_dir}")

def check_directory_structure(directory_path):
    print(f"Checking structure of directory: {directory_path}")
    passed = True
    required_files = ['plugin.py', '__init__.py', 'manifest.json', 'requirements.txt', 'plugin_base.py']
    
    for folder_name, subfolders, filenames in os.walk(directory_path):
        print(f"Directory: {folder_name}")
        for subfolder in subfolders:
            print(f"  Subdirectory: {subfolder}")
        for filename in filenames:
            if filename in required_files:
                print(f"  File: {filename} (passed)")
            else:
                print(f"  File: {filename}")
                passed = False

    if passed:
        print("All required files are present.")
    else:
        print("Some required files are missing or additional files were found.")

def zip_directory(directory_path, output_zip_path):
    manifest_path = os.path.join(directory_path, 'manifest.json')
    if not os.path.exists(manifest_path):
        print(f"Warning: No manifest.json file found in {directory_path}. The directory will not be zipped.")
        return
    
    if not validate_manifest(manifest_path):
        print(f"Error: Invalid manifest.json file in {directory_path}. The directory will not be zipped.")
        return

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for folder_name, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                zip_file.write(file_path, os.path.relpath(file_path, directory_path))
    print(f"Directory '{directory_path}' has been zipped to '{output_zip_path}'.")

def validate_manifest(manifest_path):
    try:
        with open(manifest_path, 'r') as file:
            manifest = json.load(file)
        required_fields = ["name", "version", "game_version", "python_version"]

        for field in required_fields:
            if field not in manifest:
                print(f"Manifest is missing required field: {field}")
                return False

        return True

    except json.JSONDecodeError:
        print(f"Error: Unable to parse manifest file '{manifest_path}'.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Algorithm Plugin Manager")
    parser.add_argument('action', choices=['create', 'check', 'zip'], help="Action to perform")
    parser.add_argument('--directory', type=str, help="Path to the plugin directory")
    parser.add_argument('--output', type=str, help="Path to the output zip file")
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_plugin_structure()
    elif args.action == 'check':
        if args.directory:
            check_directory_structure(args.directory)
        else:
            print("Error: Directory path is required for checking.")
    elif args.action == 'zip':
        if args.directory and args.output:
            zip_directory(args.directory, args.output)
        else:
            print("Error: Both directory path and output zip file path are required for zipping.")

if __name__ == "__main__":
    main()
