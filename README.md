# arXiv-script (_axs_) v0.1
The [arXiv](www.arxiv.org) is the most important open-access repository for preprints in various sciences, e.g. Computer Science, Mathematics and Physics. Each preprint has its unique [arXiv identifier](https://arxiv.org/help/arxiv_identifier) (often called arXiv number). The arXiv script (_axs_) is a simple command line tool to interact with the preprint of an arXiv identifier:

- `show` print its title, authors and abstract in a terminal.
- `get` download the preprint with a standarized file name (TODO: see below).
- `bib` create a BibTeX entry for the preprint (and optionally add it to a .bib-file) to easily cite the preprint in LaTeX documents.

## example
Given the arXiv identifier `math/0211159`, let's see what we can do with it (after the installation which is explained below). Let's take a look at the preprint via
```bash
axs math/0211159 show
```
This command prints the title, author(s), abstract and arXiv subject to the terminal. If we like the article, simply change `show` to `get`. 
Then the article gets download (to the default directory, see TODO below) in the convenient formate `AUTHOR(S)-TITLE-YEAR.pdf`. For example, in this example to
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

- Pull this repository to your preferred directory via _git_ or simply copy the code. 
- In a terminal, change to the directory where you downloaded this repository to. Then create a new virtual environment, e.g. with the name `venv`, and activate it:
```bash
virtualenv venv
. venv/bin/activate
```
- Finally, install the _axs_ via
```bash
pip install --editable . 
```
<<<<<<< HEAD
In the following we will run all our commands in the virtual environment.
=======
**NOTE:** In the following we will run all our commands in this virtual environment. 
>>>>>>> 74abf556834f99eea6d247ff4d96aaae026fa0a2

## setup
After installation it is recommended to set a default directory where articles are downloaded to. This is done via
```bash
axs --set-directory PATH_TO_DIR
```
where PATH_TO_DIR is your chosen directory path. Alternatively you can give a directory for each download, see below. To set a default .bib-file, where BibTeX-entries are added to, simply use
```bash
axs --set-bib-file PATH_TO_FILE
```
Here PATH_TO_FILE is your chosen default .bib-file where your BibTeX-entries will be added to. As before, you can alternatively choose a .bib-file for each BibTeX-entry individually, see below. TODO ADD

## the commands in detail
The basic usage is the following
```bash
axs ax_id cmd flag
```
<<<<<<< HEAD
where `ax_id` is an arXiv identifier, `cmd` one of the commands below and `flag` is an (optional) flag. Note that you can get help for each command

### `show`
This command prints the title, (some of) the authors and the abstract of the corresponding arXiv preprint. The flag `-f` gives a full version, i.e. additionally all authors and the main arXiv subject.

### `get`
Simply downloads the article to your default directory (if it was already set as explained above).
=======
where `ax_id` is an arXiv identifier, `cmd` one of the commands below and `flag` is an (optional) flag. In fact, you can use several flags at once. 

The flag `--help` provides you help for each command. Note that `axs --help` gives you quick general help. 

### `show`
This command prints the title, (some of) the authors, the abstract and the main arXiv subject of the corresponding arXiv preprint. The flag `-f` gives a full version, i.e. additionally all authors and the main arXiv subject. 

### `get`
Simply downloads the article to your default directory (if it was already set as explained above) under the file name `AUTHOR(S)-TITLE-YEAR.pdf`. Two comments on the file name: 

+ For => 3 authors, we use the first author and append 'et al' as often common. 
+ The title name is shortened to TODO words to prevent too long file names. 

Before the download, the title and author(s) are printed to the terminal and there is a short countdown so that you can still cancel the download. 

With the flag `-dir` (or `--directory`) you can download the article to another directory, i.e. 
```bash
axs ax_id get -dir PATH_TO_DIR
```
downloads the article to the directory at PATH_TO_DIR. 
The flag `-o` (or `--open`) opens the preprint after the download. 
>>>>>>> 74abf556834f99eea6d247ff4d96aaae026fa0a2

### `bib`
Prints a BibTeX-entry of the article to the terminal and asks if it should be added to your default .bib-file (if it has been set before). Alternatively, use the flag `-add` (or `--add-to`) combined with the path to another .bib-file to which you want to add the BibTeX-entry. Note that at the moment, the BibTeX-entry is simply added to the end of the corresponding .bib-file.

<<<<<<< HEAD
=======
Two comments on the BibTeX-entry: 
+ The BibTeX-key, which is used to cite the preprint in a LaTeX document (`Perelman-EntropyFormulaFor-math/0211159` in our example above), is created is in the formate `AUTHOR(S)-TITLE-AX_ID` where: 
+

>>>>>>> 74abf556834f99eea6d247ff4d96aaae026fa0a2
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
