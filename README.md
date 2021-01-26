# arXiv-script (_axs_) v0.1
The [arXiv](www.arxiv.org) is the most important open-access repository for preprints in various sciences, e.g. Computer Science, Mathematics and Physics. Each preprint has its unique [arXiv identifier](https://arxiv.org/help/arxiv_identifier) (often called arXiv number). The _arXiv script_ (_axs_) is a simple command line tool to interact with the preprint of an arXiv identifier:

- `show` print its title, authors and abstract in a terminal.
- `get` download the preprint and save it with a uniform file name.
- `bib` create a BibTeX entry for the preprint (and optionally add it to a .bib-file) to easily cite the preprint in LaTeX documents.

## example
Given the arXiv identifier `math/0211159`, let's see what we can do with it (after the installation which is explained below). Let's take a look at the preprint via
```bash
axs math/0211159 show
```
This command prints the title, author(s), abstract and arXiv subject to the terminal. If we like the article, simply change `show` to `get` in the above command. 
Then the article gets downloaded (to the default directory, see below) in the convenient formate `AUTHOR(S)-TITLE-YEAR.pdf`. In this example:
```bash
Perelman-The_entropy_formula_for_the_Ricci_flow_and_its_geometric_applications-2002.pdf
```
If we decide to cite this preprint in some LaTeX document using BibTeX, simply modify the command to `axs math/0211159 bib`.
This yields the following BibTeX-entry:
```
@article{Perelman-EntropyFormulaFor-math/0211159,
	Author = {Perelman, Grisha},
	Title = {{The} entropy formula for the {Ricci} flow and its geometric applications},
	Year = {2002},
	Note = {\href{https://arxiv.org/abs/math/0211159}{arXiv:math/0211159}}
}
```
We are even asked if we want to automatically add this entry to our (default) .bib-file enabling us to cite the preprint in LaTeX right away. 

## installation
At this stage, the _axs_ is still under development. Hence we require Python (preferably =>3.0) and pip for its installation. It is also recommended to install it in a virtual environment (TODO which package?). With these requirements in place do the follwing: 

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
where PATH_TO_DIR is our chosen directory path. Alternatively we can give a directory for each download, see below. To set a default .bib-file, where BibTeX-entries are added to, simply use
```bash
axs --set-bib-file PATH_TO_FILE
```
Here PATH_TO_FILE is our chosen default .bib-file where our BibTeX-entries will be added to. As before, we can alternatively choose a .bib-file for each BibTeX-entry individually, see below.

## the commands in detail
The basic usage is the following
```bash
axs ax_id cmd flag
```
<<<<<<< HEAD
<<<<<<< HEAD
where `ax_id` is an arXiv identifier, `cmd` one of the commands below and `flag` is an (optional) flag. Note that you can get help for each command

### `show`
This command prints the title, (some of) the authors and the abstract of the corresponding arXiv preprint. The flag `-f` gives a full version, i.e. additionally all authors and the main arXiv subject.

### `get`
Simply downloads the article to your default directory (if it was already set as explained above).
=======
where `ax_id` is an arXiv identifier, `cmd` one of the commands below and `flag` is an (optional) flag. In fact, you can use several flags at once. 
=======
where `ax_id` is an arXiv identifier, `cmd` one of the commands below and `flag` is an (optional) flag. In fact, you can combine several flags. 
>>>>>>> 10758b96a0462e0062590f661d0a2d5ce2615f2f

The flag `--help` provides help for each command. Note that `axs --help` gives quick general help for the _axs_. 

### `show`
This command prints the title, (some of) the authors, the abstract and the main arXiv subject of the corresponding arXiv preprint. The flag `-f` gives a full version, i.e. additionally all authors and the main arXiv subject. 

### `get`
Simply downloads the article to your default directory (if it was already set as explained above) under the file name `AUTHOR(S)-TITLE-YEAR.pdf`. Two comments on the file name: 

+ For => 3 authors, we use the first author and append 'et al' as often common. 
+ The title name is shortened to TODO words to prevent too long file names. 

Before the download, the title and author(s) are printed to the terminal and there is a short countdown so that we can still cancel the download. 

With the flag `-dir` (or `--directory`) we can download the article to another directory, i.e. 
```bash
axs ax_id get -dir PATH_TO_DIR
```
downloads the article to the directory at PATH_TO_DIR. 
The flag `-o` (or `--open`) opens the preprint after the download. 
>>>>>>> 74abf556834f99eea6d247ff4d96aaae026fa0a2

### `bib`
Prints a BibTeX-entry of the article to the terminal and asks if it should be added to our default .bib-file (if it has been set before). Alternatively, use the flag `-add` (or `--add-to`) combined with the path to another .bib-file to which we want to add the BibTeX-entry. Note that at the moment, the BibTeX-entry is simply added to the end of the corresponding .bib-file, so it is not sorted e.g. alphabetically.

<<<<<<< HEAD
=======
Two comments on the BibTeX-entry: 
+ The BibTeX-key, which is used to cite the preprint in a LaTeX document (`Perelman-EntropyFormulaFor-math/0211159` in our example above), is created is in the formate `AUTHOR(S)-SHORT_TITLE-AX_ID` where
++ `AUTHOR(S)`: as for the file name but without white spaces.
++ `SHORT_TITLE`: created from the title by removing all articles & most common prepositions and then taking the first three words. Finally, remove all white spaces. 
++ `AX_ID`: the arXiv identifier which is added to make the BibTeX-entry unique. 
+ The BibTeX-key is reasonably concise but contains enough information so that it can be easily found with the auto-completion for citations in any modern LaTeX editor. 

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
