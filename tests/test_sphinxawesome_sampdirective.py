"""Unit Tests for the sphinxawesome.sampdirective module."""

from io import StringIO
from pathlib import Path

import pytest
from sphinx.application import Sphinx
from sphinx.testing.util import etree_parse
from sphinxawesome.sampdirective import __version__


def test_returns_version() -> None:
    """It returns the correct version."""
    assert __version__ == "1.0.0"


def test_rootdir_fixture(rootdir: Path) -> None:
    """It can access the test files."""
    conf_file = rootdir / "test-root" / "conf.py"
    index_file = rootdir / "test-root" / "index.rst"
    assert conf_file.exists()
    assert index_file.exists()


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.sphinx("xml")
def test_returns_warning_without_extension(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It returns a warning if the extension is not added to the config."""
    app.builder.build_all()

    assert 'Unknown directive type "samp"' in warning.getvalue()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")
    assert len(blocks) == 0


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_finds_samp_directives(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It does not return a warning if the extension is enabled."""
    app.builder.build_all()

    assert "" in warning.getvalue()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")
    assert len(blocks) == 5


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_parses_samp_without_placeholder_correctly(app: Sphinx) -> None:
    """It parses samp directives without placeholder."""
    app.builder.build_all()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")

    #  first block has no {REPLACE} placeholder
    test = blocks[0].findall("./emphasis")
    assert len(test) == 0


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_parses_samp_with_placeholder_correctly(app: Sphinx) -> None:
    """It parses samp directives without placeholder."""
    app.builder.build_all()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")

    #  second block has a {REPLACE} placeholder
    test = blocks[1].findall("./emphasis")
    assert len(test) == 1
    assert test[0].get("classes") == "var"


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_parses_samp_with_one_prompt(app: Sphinx) -> None:
    """It parses samp directives with a single prompt."""
    app.builder.build_all()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")

    #  third block has a "gp" class for the prompt character
    test = blocks[2].findall("./inline")
    assert len(test) == 1
    assert test[0].get("classes") == "gp"


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_parses_samp_with_two_prompts(app: Sphinx) -> None:
    """It parses samp directives with multiple prompts."""
    app.builder.build_all()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")

    #  fourth block has 2 prompts
    test = blocks[3].findall("./inline")
    assert len(test) == 2
    assert test[0].get("classes") == "gp"
    assert test[1].get("classes") == "gp"


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_parses_samp_directive_with_prompt_char_in_variable(app: Sphinx) -> None:
    """It parses samp directives with a prompt character at the beginning in a variable."""
    app.builder.build_all()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")

    #  fourth block should not have "gp", because it's not a prompt
    test = blocks[4].findall("./inline")
    assert len(test) == 0
