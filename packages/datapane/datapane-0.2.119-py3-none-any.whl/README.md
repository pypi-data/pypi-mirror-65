# Datapane CLI and Python client library

[![image](https://img.shields.io/pypi/v/datapane.svg)](https://pypi.python.org/pypi/datapane)

Datapane is a platform to rapidly build and share data-driven reports and analysis publicly on the cloud and within your organisation.

This package includes both the Datapane Python client library, and the `datapane` command-line tool.

The `datapane` tool provides CLI functionality into creating Datapanes and running scriped Datapanes.

Available to download for Windows, macOS, and Linux. Free software under the Apache license.

Happy hacking! :)

### Docs

See https://docs.datapane.com/api/

### Install

```bash
$ pip3 install datapane
```

### Configure

```bash
$ datapane login
$ datapane ping
```

### Use

#### API

```python
from datapane import api

api.init()

ds = api.Dataset.upload_df(df)

s = api.Script.upload_file("./script.ipynb")

asset = api.Asset.upload_obj(my_matplotlib_figure)

api.Report.create(ds, asset)
```

#### Command line

```bash
# create a Dataset
$ datapane dataset upload ./test.csv --public
# create a Script
$ datapane script upload ./script.ipynb --title "My cool script"
# create a Datapane
$ datapane datapane create ./test.csv ./figure.png
```
