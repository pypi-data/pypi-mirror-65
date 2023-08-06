import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="merlin-py",
    version="1.0.0",
    description="Read the merlin-py tutorials for use...",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kellen-t-oconnor/merlin-py",
    author="Kellen O'Connor",
    author_email="kellen.t.oconnor@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["merlin-pull"],
    include_package_data=True,
    install_requires=["camelot","tabula-py"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
