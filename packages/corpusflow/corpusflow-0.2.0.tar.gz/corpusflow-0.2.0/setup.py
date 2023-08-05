#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "numpy",
    "google-cloud-translate",
    "requests",
    "micro_toolkit",
    "tenacity",  # for Baidu API QPS control
    "tokenizer_tools",
    "mistletoe",
]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="CorpusFlow is an open source platform for Neural Language Processing. It has a comprehensive, flexible ecosystem of tools, libraries and community resources that lets researchers push the state-of-the-art in NLP and developers easily build and deploy NLP powered applications.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="corpusflow",
    name="corpusflow",
    packages=find_packages(include=["corpusflow", "corpusflow.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/howl-anderson/corpusflow",
    version="0.2.0",
    zip_safe=False,
)
