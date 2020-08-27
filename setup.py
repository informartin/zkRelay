from setuptools import setup, find_packages

setup(
    name='cli',
    version='0.1',
    py_modules=find_packages(),
    install_requires=[
        'Click',
        'python-bitcoinrpc==1.0',
        'bitstring==3.1.5',
        'toml'
    ],
    entry_points='''
        [console_scripts]
        zkRelay-cli=cli:zkRelay_cli
    ''',
)