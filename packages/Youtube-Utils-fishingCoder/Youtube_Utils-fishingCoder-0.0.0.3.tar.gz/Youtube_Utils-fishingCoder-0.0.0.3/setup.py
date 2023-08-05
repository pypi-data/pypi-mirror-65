import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Youtube_Utils-fishingCoder",
    version="0.0.0.3",
    author="Max Fritzler",
    author_email="RaoulArdens1200@gmail.com",
    description="Utilities to load comments and subtitles into SQLite databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/utilities",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: Public Domain",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
                  ],
    provides=['hours.of.debugging.fun'],
    install_requires=[
        "youtube-dl",
        "json",
        "pysubs2",
        "sqlite3",
        "requests",
        "BeautifulSoup",
    ],
    python_requires='>=3.3',
)

