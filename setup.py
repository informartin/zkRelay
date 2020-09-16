from setuptools import setup, find_packages

setup(
    name='cli',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'wheel',
        'Click',
        'python-bitcoinrpc==1.0',
        'bitstring==3.1.5',
        'toml',
        'colorama',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        zkRelay=zkRelay_cli.cli:zkRelay_cli
    ''',
)