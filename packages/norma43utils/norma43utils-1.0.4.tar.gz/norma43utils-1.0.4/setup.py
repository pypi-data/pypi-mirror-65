import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="norma43utils",
    version="1.0.4",
    license="MIT",
    author="Sergi Espinar",
    author_email="sergief@users.noreply.github.com",
    description="Utils for norma43 files, like exporting to Google Spreadsheets or CSV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergief/norma43utils",
    packages=setuptools.find_packages(),
    keywords=["norma43", "utils", "bank", "account", "n43", "csb", "google", "spreadsheets", "csv"],
    scripts=["bin/norma43utils-bin"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=[
        "norma43parser >= 1.1.2, < 2.0.0",
        "google-api-python-client >= 1.8.0, < 1.9.0",
        "google-auth-httplib2 >= 0.0.3, < 0.1.0",
        "google-auth-oauthlib >= 0.4.1, < 0.5.0",
    ],
)
