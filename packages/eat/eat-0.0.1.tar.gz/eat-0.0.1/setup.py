from setuptools import setup

setup(
    name='eat',
    version='0.0.1',
    description='tool for data processing pipelines',
    url='https://github.com/frnsys/eat',
    author='Francis Tseng',
    author_email='f@frnsys.com',
    license='MIT',

    packages=['eat'],
    install_requires=[
        'PyYAML==3.12',
    ],
    entry_points='''
        [console_scripts]
        eat=eat.cli:cli
    ''',
)
