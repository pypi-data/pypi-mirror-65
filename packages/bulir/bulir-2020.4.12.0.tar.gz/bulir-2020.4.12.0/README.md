# [Brazilian UF Lawsuit IDs Retriever (BULIR)](https://github.com/ayharano/bulir)

by [Alexandre Harano](https://ayharano.dev/)

> Brazilian UF Lawsuit IDs in no time!

[![image](https://img.shields.io/pypi/v/bulir.svg)](https://python.org/pypi/bulir)
[![image](https://img.shields.io/pypi/l/bulir.svg)](https://python.org/pypi/bulir)
[![image](https://img.shields.io/pypi/pyversions/bulir.svg)](https://python.org/pypi/bulir)

------------------------------------------------------------------------

**[Brazilian UF Lawsuit IDs Retriever (BULIR)](https://gitlab.com/ayharano/bulir)** help you to retrieve Lawsuit IDs from Brazilian UF's gazettes in a specific date range for one or more UF.

This program is tailored designed to use [Jusbrasil](https://www.jusbrasil.com.br/) as its data source.

You are free to copy, modify, and distribute this application with attribution under the terms of the MIT license. See [the LICENSE file](/LICENSE) for details.

## Installation

Install and update using [`pip`](https://pip.pypa.io/en/stable/quickstart/):

    $ pip install -U bulir

BULIR requires [NodeJS](https://nodejs.org/) version 10 or above to solve JavaScript challenges from [Cloudflare](https://www.cloudflare.com/).

## Usage

```
$ bulir

Usage: bulir [OPTIONS] UF_CODE...

  Retrieves Brazilian UF lawsuit identifications.

  UF_CODE is one or more UF code to be retrieved from.

Options:
  -V, --version                Show the version and exit.
  -h, --help                   Show this message and exit.
  -s, --start-date [%Y-%m-%d]  Starting date to retrieve from gazettes.
                               Defaults to today.
  -d, --days INTEGER           Days to retrieve from gazettes. Defaults to 1.
```

## Links

- Website: https://github.com/ayharano/bulir
- License: MIT
- Releases: https://pypi.org/project/bulir/
- Code: https://github.com/ayharano/bulir
- Issue tracker: https://github.com/ayharano/bulir/issues

