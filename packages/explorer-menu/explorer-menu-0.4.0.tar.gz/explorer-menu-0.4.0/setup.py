import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as v:
    version = v.read().strip()

setuptools.setup(
    name="explorer-menu",
    version=version,
    author="Anderson Brandao",
    author_email="anderson.brands@gmail.com",
    description="A python module to help creating explorer menus for Windows Explorer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andersonbrands/explorer-menu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
