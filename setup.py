"""setup.py"""

from codecs import open as codecs_open
from setuptools import setup

with codecs_open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='mipy',
    version='0.0.1',
    description='Copy files to Micropython',
    long_description=readme,
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    url='https://github.com/bcb/mipy',
    license='MIT',
    py_modules=['mipy'],
    install_requires=['click', 'pyserial'],
    entry_points='''
        [console_scripts]
        mipy=mipy:cli
    ''',
)
