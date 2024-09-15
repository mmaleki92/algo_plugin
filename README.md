# algo-plugin

`algo-plugin` is a tool to create, check, and zip plugin directories for your application.

## Installation

You can install the package using pip:

```bash
pip install .


# Create a Plugin

```bash
algo-plugin create
```

# Check Directory Structure
```bash
algo-plugin check --directory path/to/plugin_directory
```

# Zip Directory
```bash
algo-plugin zip --directory path/to/plugin_directory --output path/to/output_zip_file.zip
```


# plugins zip structure 
```
my_plugin.zip
├── my_plugin/
│   ├── __init__.py            # Required for Python module
│   ├── my_plugin.py           # The main plugin Python file (implements PluginBase)
│   ├── assets/                # Directory for any assets used by the plugin
│       ├── image.png          # Example image file
│       ├── sound.mp3          # Example sound file
│       └── data.json          # Example data file
└── manifest.json              # A manifest file with metadata (optional)
```

the code classes should have an argument of screen likethis:
`def __init__(self, screen):`
or
`def __init__(self, **kwargs):`