import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="bearlib-py",
    version="0.3.2",
    author="eragon5779",
    author_email="eragon5779@gmail.com",
    description="Utilities and standardizations for UNCO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eragon5779/bearlib",
    packages=[
        "bearlib",
        "bearlib.logging",
        "bearlib.oracle",
        "bearlib.argparse",
        "bearlib.notifiers",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
