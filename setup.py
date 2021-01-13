from setuptools import setup

setup(
    name = 'axs',
    version = '0.1',
    py_modules = ['arxiv_script', 'article', 'retrieve', 'path_control'],
    install_requires = ['Click',],
    entry_points='''
        [console_scripts]
        axs = arxiv_script:cli
    ''', # script is called in console via 'axs'
)
