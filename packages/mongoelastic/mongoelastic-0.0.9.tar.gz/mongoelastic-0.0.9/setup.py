import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mongoelastic",
    version="0.0.9",
    author="Naim Malek",
    author_email="naim@peerbits.com",
    description="MongoDB to Elasticsearch. Through this you can import data from mongoDB to elasticsearch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naimmalek/mongoelastic",
    download_url="https://pypi.org/project/mongoelastic/",
    packages=setuptools.find_packages(),
    install_requires=["progress >= 1.5",
                      "elasticsearch >=7.6.0",
                      "pymongo >=3.10.1"
                      ],
    keywords=[
        "mongodb",
        "elasticsearch import",
        "import mongodb to elasticsearch",
        "elasticsearch",
        "import mogno to es",
        "import big data elasticsearch",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    license="MIT",

)
