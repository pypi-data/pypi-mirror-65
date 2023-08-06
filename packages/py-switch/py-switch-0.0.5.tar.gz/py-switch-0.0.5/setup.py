import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-switch",
    version='0.0.5',
    author="Reglament989",
    author_email="officialreglament989@protonmail.ch",
    description="Small tools for other languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reglament989/IniTools",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
