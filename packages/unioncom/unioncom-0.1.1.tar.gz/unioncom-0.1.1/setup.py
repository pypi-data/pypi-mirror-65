from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "unioncom",
    version = "0.1.1",
    keywords = ("unioncom", "caokai", "amss"),
    description = "unioncom: multimodal data integration method",
    python_requires=">=3.6",
    license = "MIT Licence",

    url = "https://github.com/caokai1073/unioncom",
    author = "caokai",
    author_email = "caokai@amss.ac.cn",

    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    platforms = "any",
)
