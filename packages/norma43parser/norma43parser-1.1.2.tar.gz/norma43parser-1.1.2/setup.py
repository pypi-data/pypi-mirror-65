import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="norma43parser",
    version="1.1.2",
    license="MIT",
    author="Sergi Espinar",
    author_email="sergief@users.noreply.github.com",
    description="Parser for Bank Account information files formatted in Norma 43",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergief/norma43parser",
    packages=setuptools.find_packages(),
    keywords=["norma43", "parser", "bank", "account", "n43", "csb"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
)
