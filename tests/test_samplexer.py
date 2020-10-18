"""Unit tests for the SampLexer class."""

from typing import List, Tuple

import pygments
from pygments.token import Generic, Text

from sphinxawesome.sampdirective import SampLexer


def tokenize(test: str) -> Tuple[List[pygments.token._TokenType], List[str]]:
    """Given a string, lex it with the SampLexer.

    It returns a tuple of lists with types and tokens.
    """
    tok = [(i, j) for i, j in pygments.lex(test, SampLexer())]
    types = [t for t, _ in tok]
    tokens = [t for _, t in tok]
    return types, tokens


def test_no_highlight() -> None:
    """It lexes a string with only text elements."""
    types, tokens = tokenize("Nothing to highlight")

    assert len(tokens) == len(types) == 2
    assert types == [Text, Text]
    assert tokens == ["Nothing to highlight", "\n"]


def test_single_placeholder() -> None:
    """It parses a string with a single placeholder correctly."""
    types, tokens = tokenize("emphasize {THIS}")

    assert len(tokens) == len(types) == 5
    assert types == [Text, Generic.Punctuation, Generic.Emph, Generic.Punctuation, Text]
    assert tokens == ["emphasize ", "{", "THIS", "}", "\n"]


def test_parses_prompt() -> None:
    """It parses a string with a prompt character correctly."""
    types, tokens = tokenize("$ beginning prompt, $VAR in the middle")

    assert len(tokens) == len(types) == 3
    assert types == [Generic.Prompt, Text, Text]
    assert tokens == ["$ ", "beginning prompt, $VAR in the middle", "\n"]


def test_parse_multiline_prompts() -> None:
    """It parses a string with two prompt characters.

    This also checks for alternate prompt characters.
    """
    types, tokens = tokenize("# first line\n~ second line")

    assert len(tokens) == len(types) == 6
    assert types == [Generic.Prompt, Text, Text, Generic.Prompt, Text, Text]
    assert tokens == ["# ", "first line", "\n", "~ ", "second line", "\n"]


def test_parse_variable_at_beginning() -> None:
    """It parses a variable at the beginning not as prompt."""
    types, tokens = tokenize("$HOME should not be highlighted.")

    assert len(tokens) == len(types) == 2
    assert types == [Text, Text]
    assert tokens == ["$HOME should not be highlighted.", "\n"]


def test_parse_complicated() -> None:
    """It parses a more complex pattern."""
    types, tokens = tokenize("$ parse /path/to/{THIS}/")

    assert len(tokens) == len(types) == 7
    assert types == [
        Generic.Prompt,
        Text,
        Generic.Punctuation,
        Generic.Emph,
        Generic.Punctuation,
        Text,
        Text,
    ]
    assert tokens == ["$ ", "parse /path/to/", "{", "THIS", "}", "/", "\n"]


def text_parse_two_placeholders() -> None:
    """It parses two placeholders."""
    types, tokens = tokenize("Parse {THIS} and {THAT}")

    assert len(tokens) == len(types) == 9
    assert types == [
        Text,
        Generic.Punctuation,
        Generic.Emph,
        Generic.Punctuation,
        Text,
        Generic.Punctuation,
        Generic.Emph,
        Generic.Punctuation,
        Text,
    ]
    assert tokens == ["Parse ", "{", "THIS", "}", " and ", "{", "THAT", "}", "\n"]


def test_parse_empty_curly_braces() -> None:
    """It parses empty curly braces as text."""
    types, tokens = tokenize("Empty {} are text.")

    assert len(types) == len(tokens) == 4
    assert types == [Text] * 4
    assert tokens == ["Empty ", "{", "} are text.", "\n"]


def test_open_curly_brace() -> None:
    """It parses open curly brace as text."""
    types, tokens = tokenize("Open { is text.")

    assert len(types) == len(tokens) == 4
    assert types == [Text] * 4
    assert tokens == ["Open ", "{", " is text.", "\n"]


def test_escaped_curly_braces() -> None:
    """It parses escaped curly braces as text."""
    types, tokens = tokenize(r"Do not \{HIGHLIGHT\}.")

    assert len(types) == len(tokens) == 6
    assert types == [Text] * 6
    assert tokens == ["Do not ", "\\{", "HIGHLIGHT", "\\}", ".", "\n"]


def test_nested_placeholder() -> None:
    """It parses a placeholder in a nested escaped curly brace."""
    types, tokens = tokenize(r"\{{THIS}\}")

    assert len(types) == len(tokens) == 6
    assert types == [
        Text,
        Generic.Punctuation,
        Generic.Emph,
        Generic.Punctuation,
        Text,
        Text,
    ]
    assert tokens == ["\\{", "{", "THIS", "}", "\\}", "\n"]
