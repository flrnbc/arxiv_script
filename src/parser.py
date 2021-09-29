"""Formatter classes and functions to format article data.
"""

from abc import ABC, abstractmethod

# from typing import List

# include a 'ListParser'?


class ParserInterface(ABC):
    """Interface to parse a list of strings (typically article data)
    to output a string.
    """

    @abstractmethod
    def parse(self, data):
        pass


class ContractTitle(ParserInterface):
    """When saving articles, contracts title for more
    convenient file names via a 'cut-off'.
    """

    def parse(self, title: str) -> str:
        title_split = title.split()
        print(title_split[:14])
        contracted_title = "_".join(title_split[:15])
        return contracted_title


class ShortenAuthors(ParserInterface):
    """Parser (class) to shorten a string of authors e.g. for more convenient
    display.
    Parse method does the following:
    Input:
    - authors (str): connected by 'and'.

    Output:
    - authors_short (str): a short version of the string
      of authors with the following rules:
      2 authors: 'A and B'.
      3 authors: 'A, B and C'.
      > 3 authors: 'A et al'.
    """

    def parse(self, authors: str) -> str:
        authors_split = authors.split(" and ")
        length = len(authors_split)
        if length == 1:
            return authors_split[0]
        if 1 < length <= 3:
            authors_short_list = authors_split[:3]
            authors_short = ", ".join(authors_short_list[:-1])
            authors_short += " and " + authors_short_list[-1]
            return authors_short
        return authors_split[0] + " et al"


class ContractAuthors(ParserInterface):
    """Parser (class) to contract a string of authors e.g. for file names.
    Attribute:
    - shortener (ShortenAuthors)

    Parse method does the following:
    Input:
    - authors (str) (as for ShortenAuthors)

    Output:
    - authors_contracted (str): contracts the output of the shortener, e.g.
      'Miller and Roberts' -> 'MillerRoberts'
    """

    def __init__(self):
        self.shortener = ShortenAuthors()

    def parse(self, authors: str) -> str:
        shortened_authors = self.shortener.parse(authors)
        shortened_authors = shortened_authors.replace(",", "")
        shortened_authors = shortened_authors.replace("and", "")
        shortened_authors = shortened_authors.title()
        return shortened_authors.replace(" ", "")
