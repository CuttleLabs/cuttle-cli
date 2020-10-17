from setuptools import setup, find_packages

setup(
    name='prodo',
    version='0.0.1',
    py_modules=['prodo'],
    install_requires=[
        'Click',
        'paramiko',
        'scp',
        'nbformat'
    ],
    entry_points='''
        [console_scripts]
        prodo=script:cli
    ''',
)