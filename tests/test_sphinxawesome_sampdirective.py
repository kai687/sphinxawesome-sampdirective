import pytest
from sphinx.testing.util import etree_parse
from sphinxawesome.sampdirective import __version__


def test_version():
    """test that the version we expect is indeed here."""

    assert __version__ == "1.0.0"


def test_rootdir_fixture(rootdir):
    """
    Test basic assumptions about test files/directories.
    The test files are in './test-root'.
    """

    conf_file = rootdir / "test-root" / "conf.py"
    index_file = rootdir / "test-root" / "index.rst"
    assert conf_file.exists()
    assert index_file.exists()


@pytest.mark.sphinx("xml")
def test_samp_warning(app, status, warning):
    """
    Test that using the samp directive without adding the extension
    raises a warning and no literal_blocks are in the output.
    """

    app.builder.build_all()

    assert 'Unknown directive type "samp"' in warning.getvalue()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")
    assert len(blocks) == 0


@pytest.mark.sphinx(
    "xml", confoverrides={"extensions": ["sphinxawesome.sampdirective"]}
)
def test_samp_directive(app, status, warning):
    """Test samp directive with extension enabled"""

    app.builder.build_all()

    assert "" in warning.getvalue()

    et = etree_parse(app.outdir / "index.xml")
    blocks = et.findall("./section/literal_block")
    assert len(blocks) == 2

    # first block has no {REPLACE} placeholder
    test = blocks[0].findall("./emphasis")
    assert len(test) == 0

    # second block has a {REPLACE} placeholder
    test = blocks[1].findall("./emphasis")
    assert len(test) == 1
    assert test[0].get("classes") == "var"
