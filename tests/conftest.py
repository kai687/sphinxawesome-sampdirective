"""Common configuration and fixtures for tests."""

import pytest
from _pytest.config import Config
from sphinx.testing.path import path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir() -> path:
    """Return path of the root directory."""
    return path(__file__).parent.abspath()


def pytest_configure(config: Config) -> None:
    """Register `sphinx` marker."""
    config.addinivalue_line("markers", "sphinx")
