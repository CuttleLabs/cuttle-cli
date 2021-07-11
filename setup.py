from setuptools import setup, find_packages

setup(
    name='cuttle',
    version='0.4.2',
    author="Karishnu Poddar",
    author_email="karishnu@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'paramiko',
        'scp',
        'nbformat',
        'nbconvert',
        'ipython',
        'click-log'
    ],
    entry_points='''
        [console_scripts]
        cuttle=cuttle.cli:cli
    ''',
)