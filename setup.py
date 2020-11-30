
from setuptools import setup

setup(
    name = 'arxiv-script',
    version = '0.1',
    py_modules = ['arxiv-script', 'article', 'retrieve', 'dir_control'],
    install_requires = ['Click', 
    ],
    entry_points='''
        [console_scripts]
        arxiv-script = arxiv-script:cli
    ''',
)
