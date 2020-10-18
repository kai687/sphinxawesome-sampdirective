"""Unit Tests for the sphinxawesome.sampdirective module."""

from io import StringIO
from pathlib import Path

import pytest
from sphinx.application import Sphinx
from sphinx.testing.util import etree_parse

from sphinxawesome.sampdirective import __version__


def test_returns_version() -> None:
    """It returns the correct version."""
    assert __version__ == "1.0.4"


def test_rootdir_fixture(rootdir: Path) -> None:
    """It can access the test files."""
    conf_file = rootdir / "test-root" / "conf.py"
    index_file = rootdir / "test-root" / "index.rst"
    assert conf_file.exists()
    assert index_file.exists()


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
def test_does_not_return_warning_with_extension(
    app: Sphinx, status: StringIO, warning: StringIO
) -> None:
    """It does not return a warning if the extension is enabled."""
    app.builder.build_all()

    assert "" in warning.getvalue()


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_finds_samp_directives(app: Sphinx) -> None:
    """It finds all samp directives."""
    app.builder.build_all()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")
    assert len(blocks) == 1
    prompts = blocks[0].findall("inline")
    assert len(prompts) == 2
    assert prompts[0].get("classes") == "gp"
    emph = blocks[0].findall("emphasis")
    assert len(emph) == 1
    assert emph[0].get("classes") == "var"
