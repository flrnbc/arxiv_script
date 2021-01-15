# arXiv-script (axs) v0.1
The [arXiv](www.arxiv.org) is the most important open-access repository for preprints in various sciences, e.g. Computer Science, Mathematics and Physics. Each preprint has its unique [arXiv identifier](https://arxiv.org/help/arxiv_identifier) (often called arXiv number). The arXiv script (_axs_) is a simple command line tool to interact with the preprint of an arXiv identifier:

- `show`: print its title, authors and abstract in a terminal.
- `get`: download the preprint with a standarized file name (see TODO: below).
- `bib`: create a BibTeX entry for the preprint (and optionally add it to a .bib-file) to easily cite the preprint in LaTeX documents.

## installation
At this stage, the _axs_ is still under development 
...


## the commands in detail
After the installation of the script, the basic usage is the following 
```bash
axs ax_id cmd -flag
```
where `ax_id` is an arXiv identifier, `cmd` one of the following commands and `-flag` is an (optional) flag. 

### `show`

### `get`

### `bib`


## background

## planned features







# OLD
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
