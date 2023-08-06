import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Utilities-fishingCoder",
    version="0.0.4.5",
    author="Max Fritzler",
    author_email="RaoulArdens1200@gmail.com",
    description="Utilities for logging, imaging metadata, and miscellaneous",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/utilities",
    packages=setuptools.find_packages(),
    include_package_data=True,                      # Max added
    classifiers = [
        "Programming Language :: Python :: 3",
        # "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "License :: Public Domain",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
                  ],
    provides=['hours.of.debugging.fun'],
    install_requires=[
        "beautifulsoup4",
        "PySimpleGUI",
    ],
    python_requires='>=3.6',
)

