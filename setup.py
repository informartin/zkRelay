from setuptools import setup, find_packages

setup(
    name='cli',
    version='0.1',
    py_modules=['cli'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'wheel',
        'Click',
        'python-bitcoinrpc==1.0',
        'bitstring==3.1.5',
        'toml',
        'colorama',
        'termcolor',
        'pytest_httpserver'
    ],
    entry_points='''
        [console_scripts]
        zkRelay=cli:zkRelay_cli
    ''',
)