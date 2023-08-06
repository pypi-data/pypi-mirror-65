# `ekans` - A simple utility to check Conda environments integrity

[![builds.sr.ht status](https://builds.sr.ht/~diego/ekans.svg)](https://builds.sr.ht/~diego/ekans?)
[![PyPI version](https://badge.fury.io/py/ekans.svg)](https://badge.fury.io/py/ekans)

`ekans` is an simple set of scripts able to perform different checks on
Anaconda environments. This script is mainly thought as an easy way to
substitute the notion of development dependencies, which is lacking in Conda
environments.

Development dependencies are packages that are used during development and that
must strictly correlate with the Python version of the project. Some other
package managers (like Poetry) are able to define these dependencies to be
installed in regular environments but excluded from builds or using flags. This
is not possible in Conda: all packages in the declared environment are treated
equally, which implies this unwanted dependencies being bundled in production
as well. On the other hand, fighting against it makes the environment prone to
be non-consistent between production and development.

One way to solve this situation is having two different environments:
`env/prod.yml` and `env/dev.yml`. `ekans` is able to check that **all versions
are fixed and that production is a strict subset of development**. This results
in the desired scenario: correctly excluding the unwanted dependencies while
ensuring that both environments have the same real dependencies to test
against.

## Install

It is possible to install the package from PyPI using `pip`:

```shell
pip install --user ekans
```

## Usage

To check if an environment can be reproduced correctly, use the `verify` in the
CLI tool. Not passing `-f` will cause the command to interactively prompt the
user to enter the path to the file.

```shell
ekans verify [-f path/to/environment.yml]
```
