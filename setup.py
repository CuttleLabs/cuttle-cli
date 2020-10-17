from setuptools import setup, find_packages

setup(
    name='prodo-pkg-karishnu',
    version='0.0.1',
    author="Karishnu Poddar",
    author_email="karishnu@gmail.com",
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