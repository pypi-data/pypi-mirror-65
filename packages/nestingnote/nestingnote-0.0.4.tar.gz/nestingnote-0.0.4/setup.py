import setuptools
from sys import platform

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = []
if platform.startswith("win"):
    dependencies.append("windows-curses")

setuptools.setup(
    name="nestingnote",
    version="0.0.4",
    author="Woodson Miles",
    author_email="woodomiles@gmail.com",
    description="Terminal note-taking application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woodsonmiles/nesting-note",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    install_requires=dependencies
)
