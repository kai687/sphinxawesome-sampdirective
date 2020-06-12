"""Nox sessions."""

import tempfile
from typing import Any

import nox
from nox.sessions import Session

nox.options.sessions = ["tests"]
locations = ["src", "tests", "noxfile.py"]


def install_constrained_version(session: Session, *args: str, **kwargs: Any) -> None:
    """Install packages with version constraints from poetry.lock"""
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


@nox.session(python=["3.6", "3.7", "3.8"])
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
