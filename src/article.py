"""Contains the definition of the article class with
its basic functionality (e.g. download and bibtex-entry).
"""

import re
import time
from pathlib import Path

import requests


def escape_special_chars(string, special_chars):
    """Escape special characters via adding backslash."""
    escape_string = string
    for special_char in special_chars:
        # note that we need to escape the backslash
        escape_string = re.sub(special_char, "\\" + special_char, escape_string)

    return escape_string


def delete_prepositions(string, to_delete, case_sensitive=True):
    """Delete a list of prepositions or articles from given string.
    If case_sensitive is False, ignore if words in to_delete are
    captialized or not.
    """
    # NOTE: it doesn't work for words in to_delete if they are followed
    # e.g. by a comma. In our application, this is not a problem though.
    split_string = string.split()
    if not case_sensitive:
        to_delete_caps = [word.capitalize() for word in to_delete]
        to_delete += to_delete_caps
    for word in to_delete:
        while word in split_string:
            split_string.remove(word)

    return " ".join(split_string)


def bib_title(string):
    """Helper function to create correct title for bibtex, i.e. curly braces
    around words which contain capital letters (to actually print them capital
    in the compiled TeX-file) and escaping special characters.
    Example:
    "$N=2$ supersymmetry" -> "{$N=2$} supersymmetry"
    (this example shows that isupper() does not suffice)
    """
    caps = re.compile("[A-Z]")
    special_chars = [r'"', r"{", r"}"]
    split_string = string.split()
    split_string = [escape_special_chars(w, special_chars) for w in split_string]
    # Curly braces around words containing capital letters
    split_string = [f"{{{w}}}" if re.search(caps, w) else w for w in split_string]

    return " ".join(split_string)


class Article:
    """Article class instantiated from kwargs article_data containing
    the corresponding properties of an article.
    Note that we require a 'title' and 'authors' in article_data
    as the bare minimum.

    TODO: we do not (yet) give type hints (e.g. using pydantic).
    """

    def __init__(self, **article_data):
        try:
            article_data["title"]
            article_data["authors"]
            for key, value in article_data.items():
                setattr(self, key, value)
        except KeyError:
            print("wrong")

    def __str__(self):
        article_str = ""
        for key, value in vars(self).items():
            article_str += f"{key.title()}:\n {value}\n\n"
        return article_str

    def download(self, save_dir):
        """Download article to save_dir.
        Return the absolute path (object) of
        saved file.
        """
        # create convenient file name
        title_split = self.title.split()
        # more intelligent "cut-off" for title?
        contracted_title = "_".join(title_split[:15]) + "-" + self.year
        file_name = self.authors_contracted + "-" + contracted_title
        file_path = Path(f"{save_dir}/{file_name}.pdf")
        # request url of pdf
        pdf_url = f"https://arxiv.org/pdf/{self.ax_id}.pdf"
        r_pdf = requests.get(pdf_url)
        # download file with delay
        t_count = 3
        while t_count:
            print(
                f"Download in {t_count} second(s)" "(press Ctrl + c to cancel).",
                end="\r",
            )
            time.sleep(1)
            t_count -= 1
        # write to file
        open(file_path, "wb").write(r_pdf.content)

        # return the absolute file path (object)
        return file_path.resolve()

    def bib_key(self):
        """Create a convenient bibtex entry.
        For authors: `Contract' the short authors' name, i.e. remove
        white space and capitalize 'et al' (if present).
        For title: Remove commas as well as all common propositions and
        articles (i.e. 'on', 'in', 'a', 'the', ...); then take the first
        three words.
        The arXiv identifier is added at the end to guarantee uniqueness.
        """
        # key for authors
        authors_key = self.authors_contracted
        # key for title
        # remove most common propositions and articles
        to_remove = ["a", "and", "in", "of", "on", "or", "the", "for"]
        title_key = delete_prepositions(self.title, to_remove, case_sensitive=False)
        # remove characters which are not allowed/unnecessary in bibtex key
        remove_chars = re.compile(r'[\\{},~#%:"]')
        title_key = re.sub(remove_chars, "", title_key)
        title_key_split = title_key.split()
        title_key = "".join(t.capitalize() for t in title_key_split[:3])

        return authors_key + "-" + title_key + "-" + self.ax_id

    def bib(self):
        """Create a bibtex entry for the given article using
        bib_key and bib_tile.
        """
        article_key = self.bib_key()
        url = f"https://arxiv.org/abs/{self.ax_id}"
        title = bib_title(self.title)
        bib_entry = (
            f"@article{{{article_key},\n\tAuthor = {{{self.authors}}},"
            f"\n\tTitle = {{{title}}},"
            f"\n\tYear = {{{self.year}}},"
            f"\n\tNote = {{\\href{{{url}}}{{arXiv:{self.ax_id}}}}}\n}}"
        )
        return bib_entry
