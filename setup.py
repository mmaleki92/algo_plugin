from setuptools import setup, find_packages

setup(
    name='algo-plugin',
    version='0.1',
    description='A tool to create, check, and zip plugin directories.',
    author='Morteza Maleki',
    author_email='algogame.py@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'algo-plugin=algo_plugin.cli:main',
        ],
    },
    install_requires=[],
    python_requires='>=3.6',
)
