"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

nox.options.stop_on_first_error = True
nox.options.sessions = ["tests", "lint", "mypy", "pytype", "safety"]
locations = ["src", "tests", "noxfile.py"]
python_versions = ["3.6", "3.7", "3.8", "3.9"]


def install_constrained_version(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages with version constraints from poetry.lock."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            "--without-hashes",
            "--dev",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=python_versions)
@nox.parametrize("sphinx", ["2.*", "3.*"])
def tests(session: Session, sphinx: str) -> None:
    """Run unit tests."""
    args = session.posargs or ["--cov"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_constrained_version(session, "coverage[toml]", "pytest", "pytest-cov")
    session.run("poetry", "run", "pip", "install", f"sphinx=={sphinx}", external=True)
    session.run("pytest", *args)
    session.run(
        "poetry",
        "run",
        "python",
        "-c",
        "import sphinx; print(sphinx.__version__)",
        external=True,
    )


@nox.session(python=python_versions)
def lint(session: Session) -> None:
    """Lint with Flake8."""
    args = session.posargs or locations
    install_constrained_version(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "flake8-implicit-str-concat",
    )
    session.run("flake8", *args)


@nox.session(python=python_versions)
def mypy(session: Session) -> None:
    """Check types with mypy."""
    args = session.posargs or locations
    install_constrained_version(session, "mypy")
    session.run("mypy", *args)


@nox.session(python=[v for v in python_versions if float(v) < 3.9])
def pytype(session: Session) -> None:
    """Check types with pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_constrained_version(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=python_versions)
def typeguard(session: Session) -> None:
    """Check types at runtime with typeguard."""
    package = "sphinxawesome.sampdirective"
    session.run("poetry", "install", "--no-dev", external=True)
    install_constrained_version(session, "pytest", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@nox.session(python="3.9")
def safety(session: Session) -> None:
    """Check for insecure dependencies with safety."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        install_constrained_version(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python="3.9")
def coverage(session: Session) -> None:
    """Upload coverage report."""
    install_constrained_version(session, "coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox.session(python="3.9")
def black(session: Session) -> None:
    """Format code with Black."""
    args = session.posargs or locations
    install_constrained_version(session, "black")
    session.run("black", *args)
