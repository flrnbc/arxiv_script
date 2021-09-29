import src.parser as sp

title = (
    "This is a very fancy title with a lot of words and some symbols:"
    " {}, ''! And so on an so forth..."
)


def test_ContractTitle():
    contract_title = sp.ContractTitle()
    title_contracted = contract_title.parse(title)
    assert title_contracted == (
        "This_is_a_very_fancy_title_with_a_lot_of" "_words_and_some_symbols:_{},"
    )


authors = "The first and the second and the third and the fourth genius"
authors2 = "da Vinci"
authors3 = "da Vinci and Michelangelo"
authors4 = "Donatello and da Vinci and Michelangelo"


def test_ShortenAuthors():
    shorten_authors = sp.ShortenAuthors()
    assert shorten_authors.parse(authors) == "The first et al"
    assert shorten_authors.parse(authors2) == "da Vinci"
    assert shorten_authors.parse(authors3) == "da Vinci and Michelangelo"
    assert shorten_authors.parse(authors4) == "Donatello, da Vinci and Michelangelo"


def test_ContractAuthors():
    contract_authors = sp.ContractAuthors()
    assert contract_authors.parse(authors) == "TheFirstEtAl"
    assert contract_authors.parse(authors2) == "DaVinci"
    assert contract_authors.parse(authors3) == "DaVinciMichelangelo"
    assert contract_authors.parse(authors4) == "DonatelloDaVinciMichelangelo"
