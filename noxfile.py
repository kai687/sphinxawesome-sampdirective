"""Nox sessions."""

import tempfile

import nox
from nox_poetry import Session, session

nox.options.stop_on_first_error = True
nox.options.sessions = ["tests", "lint", "mypy", "safety"]
locations = ["src", "tests", "noxfile.py"]
python_versions = ["3.7", "3.8", "3.9", "3.10"]


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    deps = ["coverage[toml]", "pytest", "pytest-cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install(".", *deps)
    session.run("pytest", *args)


@session(python=python_versions)
def lint(session: Session) -> None:
    """Lint with Flake8."""
    args = session.posargs or locations
    deps = [
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-implicit-str-concat",
    ]
    session.install(".", *deps)
    session.run("flake8", *args)


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Check types with mypy."""
    args = session.posargs
    deps = ["mypy", "types-docutils", "pytest", "sphinx", "nox", "nox-poetry"]
    session.install(".", *deps)
    session.run("mypy", *args)


@session(python=python_versions)
def typeguard(session: Session) -> None:
    """Check types at runtime with typeguard."""
    package = "sphinxawesome.sampdirective"
    deps = ["pytest", "typeguard"]
    session.install(".", *deps)
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@session(python=python_versions[-1])
def safety(session: Session) -> None:
    """Check for insecure dependencies with safety."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    session.run("safety", "check", f"--file={requirements}", "--full-report")


@session(python=python_versions[-1])
def coverage(session: Session) -> None:
    """Upload coverage report."""
    session.install(".", "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@session(python=python_versions[-1])
def black(session: Session) -> None:
    """Format code with Black."""
    args = session.posargs or locations
    session.install(".", "black")
    session.run("black", *args)


@session(python=python_versions[-1])
def isort(session: Session) -> None:
    """Reorder imports with isort."""
    args = session.posargs or locations
    session.install(".", "isort")
    session.run("isort", *args)
