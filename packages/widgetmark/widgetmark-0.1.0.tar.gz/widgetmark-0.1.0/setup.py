"""
setup.py for widgetmark.

For reference see
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
from pathlib import Path
from setuptools import setup, PEP420PackageFinder

find_packages = PEP420PackageFinder.find


HERE = Path(__file__).parent.absolute()
with (HERE / "README.md").open("rt") as fh:
    LONG_DESCRIPTION = fh.read().strip()


REQUIREMENTS: dict = {
    "core": [
        "PyQt5",
        "QtPy",
        "numpy",
        "scipy",
        "pyqtgraph",
        "matplotlib",
        "dataclasses;python_version<'3.7'",
        "snakeviz",
    ],
    "testing": [
        "pytest~=4.4.0",
        "pytest-qt~=3.2.0",
        "pytest-cov~=2.5.1",
        "pytest-random-order~=1.0.4",
    ],
    "doc": [
        "Sphinx~=2.1.2",
        "recommonmark~=0.6.0",
        "sphinx-rtd-theme~=0.4.3",
    ],
    "linting": [
        "mypy~=0.720",
        "pylint>=2.3.1&&<3",
        "pylint-unittest>=0.1.3&&<2",
        "flake8>=3.7.8&&<4",
        "flake8-quotes>=2.1.0&&<3",
        "flake8-commas>=2&&<3",
        "flake8-colors>=0.1.6&&<2",
        "flake8-rst>=0.7.1&&<2",
        "flake8-breakpoint>=1.1.0&&<2",
        "flake8-pyi>=19.3.0&&<20",
        "flake8-comprehensions>=2.2.0&&<3",
        "flake8-builtins-unleashed>=1.3.1&&<2",
        "flake8-blind-except>=0.1.1&&<2",
        "flake8-bugbear>=19.8.0&&<20",
    ],
    "release": [
        "twine~=1.13.0",
        "wheel~=0.33.4",
    ],
}


setup(
    name="widgetmark",
    version="0.1.0",

    author="Fabian Sorn",
    author_email="fabian.sorn@icloud.com",
    description="Benchmarking Framework for Qt Widgets.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/fabianSorn/widgetmark",
    download_url="https://github.com/fabianSorn/widgetmark/archive/v0.1.tar.gz",

    entry_points={
        "console_scripts": ["widgetmark = widgetmark.cli:main"],
    },

    packages=find_packages(),
    python_requires=">=3.6, <4",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    install_requires=REQUIREMENTS["core"],
    extras_require={
        **REQUIREMENTS,
        # The "dev" extra is the union of "graph" and "doc", with an option
        # to have explicit development dependencies listed.
        "dev": [req
                for extra in ["dev", "testing", "linting", "doc"]
                for req in REQUIREMENTS.get(extra, [])],
        # The "all" extra is the union of all requirements.
        "all": [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
)
