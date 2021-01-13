# arXiv-script (axs)
## background
The arXiv (www.arxiv.org) is the most important open-access repository for electronic preprints in various sciences, e.g. Computer Science, Mathematics and Physics. Even though it is 'only' moderated and not peer-reviewed, ...

## the script
The arXiv script (axs) is a simple command line tool to view and download arXiv


## FUNCTIONALITY
show arxiv article, ask for download (slow delay) (and/or open file)
arxiv get ARXIV_NO
flags: --open (open after download)

show article
arxiv show ARXIV_NO

change directory where files are donwloaded to
arxiv --dir


## ADVANCED
- get bibtex (--bib ?)
- check with zentralblatt (equivalent for other disciplines?)
- check recent/day submissions of a specific subject
(- add possibility to save different identifiers in different folders)


## TODO
- dir_control function: so far only macOS...
- understand setuptools, in particular dependencies of modules/packages
