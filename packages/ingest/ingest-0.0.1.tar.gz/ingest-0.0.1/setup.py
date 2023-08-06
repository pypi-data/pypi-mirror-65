from setuptools import setup

setup(
    name='ingest',
    version='0.0.1',
    description='tool for data processing pipelines',
    url='https://github.com/frnsys/ingest',
    author='Francis Tseng',
    author_email='f@frnsys.com',
    license='MIT',

    packages=['ingest'],
    install_requires=[
        'PyYAML==3.12',
    ],
    entry_points='''
        [console_scripts]
        ingest=ingest.cli:cli
    ''',
)
