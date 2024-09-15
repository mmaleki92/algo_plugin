import os
import json
import pytest
import zipfile
import tempfile
from your_script_name import create_plugin_structure, check_directory_structure, zip_directory, validate_manifest

# Helper function to create a temporary directory
def create_temp_dir():
    temp_dir = tempfile.mkdtemp()
    return temp_dir

# Helper function to remove a directory tree
def remove_dir_tree(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

def test_create_plugin_structure():
    temp_dir = create_temp_dir()
    os.chdir(temp_dir)  # Change to the temporary directory
    
    # Run the plugin creation function
    create_plugin_structure()
    
    # Check the presence of expected files and directories
    plugin_dir = os.path.join(temp_dir, 'plugins')
    assert os.path.isdir(plugin_dir)
    
    plugin_name = 'TestPlugin'
    plugin_dir = os.path.join(plugin_dir, plugin_name)
    assert os.path.isdir(plugin_dir)
    assert os.path.isfile(os.path.join(plugin_dir, 'manifest.json'))
    assert os.path.isfile(os.path.join(plugin_dir, '__init__.py'))
    assert os.path.isfile(os.path.join(plugin_dir, 'plugin.py'))
    assert os.path.isfile(os.path.join(plugin_dir, 'requirements.txt'))
    assert os.path.isfile(os.path.join(plugin_dir, 'plugin_base.py'))
    
    with open(os.path.join(plugin_dir, 'manifest.json')) as f:
        manifest = json.load(f)
    assert 'name' in manifest
    assert 'version' in manifest
    assert 'game_version' in manifest
    assert 'python_version' in manifest

    remove_dir_tree(temp_dir)

def test_check_directory_structure():
    temp_dir = create_temp_dir()
    plugin_name = 'TestPlugin'
    plugin_dir = os.path.join(temp_dir, 'plugins', plugin_name)
    os.makedirs(plugin_dir)
    
    # Create expected files
    with open(os.path.join(plugin_dir, 'plugin.py'), 'w') as f:
        f.write('')
    with open(os.path.join(plugin_dir, '__init__.py'), 'w') as f:
        f.write('')
    with open(os.path.join(plugin_dir, 'manifest.json'), 'w') as f:
        json.dump({
            "name": plugin_name,
            "version": "1.0.0",
            "description": f"A plugin for {plugin_name}.",
            "game_version": "1.0",
            "python_version": "3.8",
            "dependencies": [],
            "author": "Author",
            "contact": "Contact"
        }, f, indent=4)
    with open(os.path.join(plugin_dir, 'requirements.txt'), 'w') as f:
        f.write('')
    with open(os.path.join(plugin_dir, 'plugin_base.py'), 'w') as f:
        f.write('class PluginBase: pass\n')

    # Check directory structure
    check_directory_structure(plugin_dir)
    
    remove_dir_tree(temp_dir)

def test_zip_directory():
    temp_dir = create_temp_dir()
    plugin_name = 'TestPlugin'
    plugin_dir = os.path.join(temp_dir, 'plugins', plugin_name)
    os.makedirs(plugin_dir)
    
    # Create expected files
    with open(os.path.join(plugin_dir, 'plugin.py'), 'w') as f:
        f.write('')
    with open(os.path.join(plugin_dir, '__init__.py'), 'w') as f:
        f.write('')
    with open(os.path.join(plugin_dir, 'manifest.json'), 'w') as f:
        json.dump({
            "name": plugin_name,
            "version": "1.0.0",
            "description": f"A plugin for {plugin_name}.",
            "game_version": "1.0",
            "python_version": "3.8",
            "dependencies": [],
            "author": "Author",
            "contact": "Contact"
        }, f, indent=4)
    with open(os.path.join(plugin_dir, 'requirements.txt'), 'w') as f:
        f.write('')
    with open(os.path.join(plugin_dir, 'plugin_base.py'), 'w') as f:
        f.write('class PluginBase: pass\n')

    zip_path = os.path.join(temp_dir, 'plugin.zip')
    
    # Zip the directory
    zip_directory(plugin_dir, zip_path)
    
    # Check the zip file
    assert os.path.isfile(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        assert 'plugin.py' in zip_file.namelist()
        assert '__init__.py' in zip_file.namelist()
        assert 'manifest.json' in zip_file.namelist()
        assert 'requirements.txt' in zip_file.namelist()
        assert 'plugin_base.py' in zip_file.namelist()
    
    os.remove(zip_path)
    remove_dir_tree(temp_dir)

def test_validate_manifest():
    temp_dir = create_temp_dir()
    plugin_name = 'TestPlugin'
    plugin_dir = os.path.join(temp_dir, 'plugins', plugin_name)
    os.makedirs(plugin_dir)
    
    manifest_path = os.path.join(plugin_dir, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump({
            "name": plugin_name,
            "version": "1.0.0",
            "description": f"A plugin for {plugin_name}.",
            "game_version": "1.0",
            "python_version": "3.8",
            "dependencies": [],
            "author": "Author",
            "contact": "Contact"
        }, f, indent=4)
    
    assert validate_manifest(manifest_path)
    
    with open(manifest_path, 'w') as f:
        json.dump({
            "name": plugin_name,
            "version": "1.0.0",
            "description": f"A plugin for {plugin_name}.",
            "game_version": "1.0",
            "dependencies": [],
            "author": "Author",
            "contact": "Contact"
        }, f, indent=4)  # Missing python_version
    
    assert not validate_manifest(manifest_path)
    
    remove_dir_tree(temp_dir)
