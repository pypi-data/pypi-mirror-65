import setuptools
from mistermarket.mistermarket import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mistermarket",      # Replace with your own username
    version=__version__,
    author="Jero Bado",
    author_email="gerol.bado@geronacapital.com",
    description="Mr. Market - your servant in the Philippine financial market",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerobado/mistermarket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",

    ],
    python_requires='>=3.6',
)
