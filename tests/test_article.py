""" Test article.py """

from src.retrieve import get_year
import src.article as sa


def test_escape_special_chars():
    chars = [r'"', r"{"]
    test_string = '{here we go "'
    assert sa.escape_special_chars(test_string, chars) == '\\{here we go \\"'


def test_delete_prepositions():
    test1 = "Hello, a cow goes to the store."
    test2 = "Here The is capital."
    remove = ["a", "the", "to"]
    assert sa.delete_prepositions(test1, remove) == "Hello, cow goes store."
    assert sa.delete_prepositions(test2,
                                  remove,
                                  case_sensitive=False) == "Here is capital."


def test_bib_title():
    title1 = 'The fundamental Laws of the Universe'
    title2 = 'The $N=2$ of QFT'
    title3 = 'All elements of {1, 2} are natural'
    assert sa.bib_title(title1) == "{The} fundamental {Laws} of the {Universe}"
    assert sa.bib_title(title2) == "{The} {$N=2$} of {QFT}"
    assert sa.bib_title(title3) == "{All} elements of \\{1, 2\\} are natural"


def test_article_class():
    title = "New article"
    authors = "The first, the second, the third, the fourth genius"
    authors_short = "The first, the second, the third et al"
    authors_contracted = "TheFirstTheSecondTheThird"
    abstract = "Cool article!"
    ax_id = "2525.10000"
    year = get_year(ax_id)
    main_subject = "Coolest subject ever!"

    test_class = sa.Article(title, authors, authors_short,
                            authors_contracted, abstract,
                            ax_id, year, main_subject)

    assert test_class.title == title
    assert test_class.authors == authors
    assert test_class.authors_short == authors_short
    assert test_class.authors_contracted == authors_contracted
    assert test_class.abstract == abstract
    assert test_class.ax_id == ax_id
    assert test_class.year == year
    assert test_class.main_subject == main_subject

    assert test_class.bib_key() == ("TheFirstTheSecondTheThird-NewArticle"
                                    "-2525.10000")
    bib_key = test_class.bib_key()
    assert sa.bib_title(title) == "{New} article"
    bib_title = sa.bib_title(title)

    url = "https://arxiv.org/abs/{}".format(ax_id)
    bib_entry = ("@article{{{0},\n\tAuthor = {{{1}}},\n\tTitle = {{{2}}},"
                 "\n\tYear = {{{3}}},"
                 "\n\tNote = {{\\href{{{4}}}{{arXiv:{5}}}}}\n}}"
                 ).format(bib_key, authors, bib_title, year, url, ax_id)

    assert test_class.bib() == bib_entry
