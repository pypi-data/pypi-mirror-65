import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="archicad",
    version="24.2310b3",
    author="GRAPHISOFT SE",
    author_email="archicadapi@graphisoft.com",
    description="Python binding for the ARCHICAD JSON command interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://graphisoft.atlassian.net/wiki/spaces/AC24/pages/4390913/JSON%2BPython%2BAPI%2Bfor%2BARCHICAD",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    license='Apache'
)
