from setuptools import setup, find_packages

setup(
    name='zkRelay',
    version='0.1',
    py_modules=['zkRelay_cli'],
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
        'zokrates_pycrypto'
    ],
    entry_points='''
        [console_scripts]
        zkRelay=zkRelay_cli:zkRelay_cli
    ''',
)