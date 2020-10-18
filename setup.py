from setuptools import setup, find_packages

setup(
    name='prodo',
    version='0.0.2',
    author="Karishnu Poddar",
    author_email="karishnu@gmail.com",
    py_modules=['script'],
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