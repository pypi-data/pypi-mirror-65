import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ebuilder",
    version="0.2.2",
    author="Will F",
    author_email="forsbergw82@gmail.com",
    description="An upgraded version of good ol' Eebuilder, a static site generator that 'converts' Python 3 code to HTML 5.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['ebuilder'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    url='https://github.com/RhinoCodes/Ebuilder',
)
