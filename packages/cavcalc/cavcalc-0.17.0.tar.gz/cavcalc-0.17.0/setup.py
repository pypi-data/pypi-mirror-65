import os
from setuptools import setup, find_packages
import shutil


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


REQUIREMENTS = [
    "numpy",
    "matplotlib",
    "black",
    "pre-commit",
]

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Topic :: Scientific/Engineering :: Physics",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

KEYWORDS = "physics optics interferometry"


def write_config_file():
    configpath = os.path.join(
        os.environ.get("APPDATA")
        or os.environ.get("XDG_CONFIG_HOME")
        or os.path.join(os.environ["HOME"], ".config"),
        "cavcalc",
    )

    if not os.path.isdir(configpath):
        os.makedirs(configpath, exist_ok=True)

    usr_ini_file = os.path.join(configpath, "cavcalc.ini")
    if not os.path.exists(usr_ini_file):
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "cavcalc/cavcalc.ini"), usr_ini_file
        )


write_config_file()

setup(
    name="cavcalc",
    use_scm_version={"write_to": "cavcalc/version.py"},
    author="Samuel Rowlinson",
    author_email="sjr@star.sr.bham.ac.uk",
    description=("cavcalc is a program for computing optical cavity parameters."),
    url="https://gitlab.com/sjrowlinson/cavcalc",
    license="GPL",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.6",
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    project_urls={
        "Source": "https://gitlab.com/sjrowlinson/cavcalc",
        "Documentation": "https://cavcalc.readthedocs.io/en/stable/",
    },
    package_data={"cavcalc": ["_default.mplstyle", "cavcalc.ini"]},
    include_package_data=True,
    entry_points={"console_scripts": ["cavcalc = cavcalc.__main__:main"]},
)
