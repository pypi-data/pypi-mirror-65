import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frankfurt",
    version="0.1b0",
    author="Jorge E. Cardona",
    author_email="jorgeecardona@gmail.com",
    description="Frankfurt is an ORM based on SQLAlchemy and DjangoORM using asyncpg.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/jorgeecardona/frankfurt",
    packages=setuptools.find_packages(),
    install_requires=[
        'asyncpg',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Database",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"
    ],
    python_requires='>=3.6',
)
