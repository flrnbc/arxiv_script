# arXiv-script (_axs_) v0.1
The [arXiv](www.arxiv.org) is the most important open-access repository for preprints in various sciences, e.g. Computer Science, Mathematics and Physics. Each preprint has its unique [arXiv identifier](https://arxiv.org/help/arxiv_identifier) (often called arXiv number). The arXiv script (_axs_) is a simple command line tool to interact with the preprint of an arXiv identifier:

- `show` print its title, authors and abstract in a terminal.
- `get` download the preprint with a standarized file name (TODO: see below).
- `bib` create a BibTeX entry for the preprint (and optionally add it to a .bib-file) to easily cite the preprint in LaTeX documents.

## example
Given the arXiv identifier `math/0211159`, let's see what we can do with it (after the installation which is explained below): 
```bash
axs math/0211159 show
```
prints the title, authors, abstract and arXiv subject to the terminal. If we like the article, simply change `show` to `get`. 
This downloads the article (to the default directory, see TODO below) in the convenient formate `AUTHOR(S)-TITLE-YEAR.pdf`. For example, in this case to
```bash
Perelman-The_entropy_formula_for_the_Ricci_flow_and_its_geometric_applications-2002.pdf
```
If we decide to cite this preprint in some LaTeX document using BibTeX, simply change the command to 
```bash
axs math/0211159 bib
```
This yields the following BibTeX-entry:
```
@article{Perelman-EntropyFormulaFor-math/0211159,
	Author = {Perelman, Grisha},
	Title = {{The} entropy formula for the {Ricci} flow and its geometric applications},
	Year = {2002},
	Note = {\href{https://arxiv.org/abs/math/0211159}{arXiv:math/0211159}}
}
```
We are even asked if we want to automatically add this entry to our (default) .bib-file.

## installation
At this stage, the _axs_ is still under development. Hence we require Python (preferably =>3.0) and pip for its installation. It is also recommended to install it in a virtual environment (TODO which package?). With these requirements in place do the follwing: (TODO works for any OS?!?)

- git pull or copy repository
- in a terminal, change to the directory where you downloaded this repo. Then create a new virtual environment, e.g. with the name `venv`, and activate it:
```bash
virtualenv venv
. venv/bin/activate
```
- finally, install the _axs_ via
```bash
pip install --editable . TODO why?
```
In the following we will run all our commands in the virtual environment. 

## setup
After installation it is recommended to set a default directory where articles are downloaded to. This is done via 
```bash 
axs --set-directory PATH_TO_DIR
```
where PATH_TO_DIR is your chosen directory path. Alternatively you can give a directory for each download, see below.

## the commands in detail
The basic usage is the following 
```bash
axs ax_id cmd flag
```
where `ax_id` is an arXiv identifier, `cmd` one of the commands below and `flag` is an (optional) flag. Note that you can get help for each command 

### `show`
This command prints the title, (some of) the authors and the abstract of the corresponding arXiv preprint. The flag `-f` gives a full version, i.e. additionally all authors and the main arXiv subject. 

### `get`
Simply downloads the article to your default directory (if it was already set as explained above). 

### `bib`


## background
(own motivation, Click...)

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
