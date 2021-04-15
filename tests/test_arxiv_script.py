"""Testing arxiv_script.py"""
from click.testing import CliRunner
from src.arxiv_script import cli


def test_show():
    runner = CliRunner()
    result = runner.invoke(cli, ['show', 'math.GT/0309136'])
    result_full = runner.invoke(cli, ['show', '--full', 'math.GT/0309136'])
    assert result.exit_code == 0
    assert result_full.exit_code == 0
    assert "Springer fibers" in result.output
    assert "Main subject" in result_full.output


def test_settings():
    """Only test if false input gets rejected
    (for tests of actual settings, see test_path_control)
    """
    runner = CliRunner()
    result_dir = runner.invoke(cli, ['--set-directory', 'a/fantasy/path/dir'])
    result_bib = runner.invoke(cli, ['--set-bib-file', 'a/fantasy/bib/file'])
    assert result_dir.exit_code == 0
    assert result_bib.exit_code == 0
    assert "Not a correct path" in result_dir.output
    assert "Not a correct path" in result_bib.output


def test_get():
    runner = CliRunner()
    result = runner.invoke(cli, ['get', 'fantasy/ax_id'])
    result_false_dir = runner.invoke(cli, ['get', '-d', 'fantasy/dir/',
                                           '2011.02123'])
    assert result.exit_code == 0
    assert result_false_dir.exit_code == 0
    assert "Not a correct arXiv identifier." in result.output
    assert "Please give a valid absolute path" in result_false_dir.output


def test_bib():
    runner = CliRunner()
    result_false_bib = runner.invoke(cli, ['bib', '-a', 'fantasy.bib',
                                           'math.GT/0309136'])
    result_bib = runner.invoke(cli, ['bib', 'math.GT/0309136'])
    # to add: give a valid bib file
    assert result_false_bib.exit_code == 0
    assert ("The given path does not point to a bib-file"
            in result_false_bib.output)
    assert result_bib.exit_code == 0
    assert "Here is the requested BibTeX entry:" in result_bib.output
