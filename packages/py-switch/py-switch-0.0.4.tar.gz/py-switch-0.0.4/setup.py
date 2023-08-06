import setuptools
from py_switch import __version__

def check_version(way=False):
    if way:
        with open('.config', 'r') as f:
            return f.read()
    else:
        with open('.config', 'w') as f:
            f.write(py_switch.__version__)


if check_version(True) == __version__:
    raise Exception("Edit version, for deployment")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-switch",
    version=__version__,
    author="Reglament989",
    author_email="officialreglament989@protonmail.ch",
    description="Small tools for other languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reglament989/IniTools",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
