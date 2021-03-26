from setuptools import setup

setup(
    name = 'axs',
    version = '0.2',
    py_modules = ['src.arxiv_script', 'src.article', 'src.retrieve', 'src.path_control'],
    install_requires = ['Click', 'requests', 'lxml', 'python-dotenv'],
    entry_points='''
        [console_scripts]
        axs = src.arxiv_script:cli
    ''', # script is called in console via 'axs'
)
