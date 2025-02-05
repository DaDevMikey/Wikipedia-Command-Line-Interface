from setuptools import setup, find_packages

setup(
    name="wiki-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'aiohttp>=3.9.1',
        'pillow>=10.1.0',
        'rich>=13.7.0',
        'prompt_toolkit>=3.0.43',
        'click>=8.1.7',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'wiki=wiki_cli.cli:main',
        ],
    },
)
