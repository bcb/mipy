from setuptools import setup

setup(
    name='mipy',
    version='0.0.1',
    py_modules=['mpy-utils'],
    install_requires=[
        'click',
        'pyserial'
    ],
    entry_points='''
        [console_scripts]
        mipy=mipy:cli
    ''',
)
