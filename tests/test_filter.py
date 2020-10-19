"""Unit tests for the filtering of braces."""

from typing import List, Tuple

import pygments
from pygments.token import Generic, Text

from sphinxawesome.sampdirective import SampLexer, unescape


def tokenize(test: str) -> Tuple[List[pygments.token._TokenType], List[str]]:
    """Given a string, lex it with the SampLexer.

    It returns a tuple of lists with types and tokens.
    """
    s = SampLexer()
    s.add_filter(unescape())
    tok = [(i, j) for i, j in pygments.lex(test, s)]
    types = [t for t, _ in tok]
    tokens = [t for _, t in tok]
    return types, tokens


def test_filtering_braces() -> None:
    """It filters curly braces from the output."""
    types, tokens = tokenize("{THIS}")

    assert len(types) == len(tokens) == 4
    assert types == [Text, Generic.Emph, Text, Text]
    assert tokens == ["", "THIS", "", "\n"]


def test_unescape_braces() -> None:
    """It unescapes escaped curly braces."""
    types, tokens = tokenize(r"\{THIS\}")

    assert len(types) == len(tokens) == 4
    assert types == [Text] * 4
    assert tokens == ["{", "THIS", "}", "\n"]
