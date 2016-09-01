from setuptools import setup

setup(
    name='mpup',
    version='0.0.1',
    py_modules=['mpup'],
    install_requires=[
        'click',
        'pyserial'
    ],
    entry_points='''
        [console_scripts]
        mpup=mpup:cli
    ''',
)
