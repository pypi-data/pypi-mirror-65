# Norma43 Utils

[![Build status](https://github.com/sergief/norma43utils/workflows/Python%20package/badge.svg)](https://github.com/sergief/norma43utils/actions?query=workflow%3A%22Python+package%22)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)


Python cli that reads a `norma43` file and transforms it to another format.
The current options are:
* Append to a google spreadsheet
* Transform to CSV (not yet implemented)

## How to install it:

From PIP:
```bash
pip install norma43utils
```

Then, create a  OAUTH2 client credentials file `credentials.json` to use the google API from there:
* [Google Developers console](https://console.developers.google.com/apis/credentials)

Copy the credentials file to the following file path:

```bash
mkdir -p $HOME/.norma43togooglespreadsheet/google/ && cp credentials.json $HOME/.norma43togooglespreadsheet/google/ 
```

## How to use it
The PIP package creates and executable that is included in you path. Just use the CLI
```bash
usage: norma43utils [-h] input {google} output {EN,ES}

Reads a norma43 formatted document, converts it and uploads it to Google
Spreadsheets.

positional arguments:
  input       norma43 input file path
  {google}    Format to output the result
  output      Google spreadsheet document id
  {EN,ES}     Date format (EN/ES)

optional arguments:
  -h, --help  show this help message and exit
```

For instance: `norma43utils movements.n43 google document_id EN`