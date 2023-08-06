from setuptools import setup

setup(
    name='refine',
    version='0.0.1',
    description='tool for data processing pipelines',
    url='https://github.com/frnsys/refine',
    author='Francis Tseng',
    author_email='f@frnsys.com',
    license='MIT',

    packages=['refine'],
    install_requires=[
        'PyYAML==3.12',
    ],
    entry_points='''
        [console_scripts]
        recine=refine.cli:cli
    ''',
)
