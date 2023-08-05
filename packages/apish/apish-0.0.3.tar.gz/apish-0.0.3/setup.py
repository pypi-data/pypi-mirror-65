import re

import setuptools


def read_file(path):
    with open(path, "r") as handle:
        return handle.read()


def read_version():
    try:
        s = read_file("VERSION")
        m = re.match(r"v(\d+\.\d+\.\d+(-.*)?)", s)
        return m.group(1)
    except FileNotFoundError:
        return "0.0.0"


long_description = read_file("docs/source/description.rst")
version = read_version()

setuptools.setup(
    name="apish",
    description="""
    Small, opinionated library for building async REST APIs.""",
    keywords="rest http web",
    long_description=long_description,
    include_package_data=True,
    version=version,
    url="https://gitlab.com/greenhousegroup/ai/libraries/apish/",
    author="Greenhouse AI team",
    author_email="ai@greenhousegroup.com",
    package_dir={"apish": "src/apish"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    # TODO: Specify version bounds of spectacular
    install_requires=["aiohttp>=3,<4", "PyYAML>=3", "spectacular"],
    data_files=[(".", ["VERSION"])],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=4", "mock>=2.0.0"],
    packages=setuptools.find_packages("src"),
)
