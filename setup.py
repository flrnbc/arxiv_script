from setuptools import setup

setup(
    name = 'axs',
    version = '0.1',
    py_modules = ['script.arxiv_script', 'script.article', 'script.retrieve', 'script.path_control'],
    install_requires = ['Click',],
    entry_points='''
        [console_scripts]
        axs = script.arxiv_script:cli
    ''', # script is called in console via 'axs'
)
