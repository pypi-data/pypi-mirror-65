import io
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def read(*names, **kwargs):
    """Read a file."""
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


setup(
    name="bulir",
    version=read("src", "bulir", "VERSION"),
    url="https://github.com/ayharano/bulir",
    license="MIT",
    author="Alexandre Harano",
    author_email="email@ayharano.dev",
    description="Brazilian UF Lawsuit IDs in no time!",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="brazilian uf lawsuit",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    python_requires=">=3.7",
    install_requires=["cfscrape", "lxml", "yarl", "anyio", "asyncclick",],
    entry_points={
        "console_scripts": ["bulir=bulir:retrieve_brazilian_uf_lawsuit_ids"]
    },
    setup_requires=["setuptools>=43.0.0"]
    if sys.version_info >= (3, 7, 0)
    else [],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
)
