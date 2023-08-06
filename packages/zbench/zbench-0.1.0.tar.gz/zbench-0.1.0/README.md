# `zbench` <img align="right" src="https://badge.fury.io/py/zbench.svg">

This package benchmarks lossless compression algorithms like `gzip` and `bzip2`,
facilitating quick comparison of the trade-offs between disk space and CPU time on _your_ file(s).

It is implemented in Python and provides a command line tool, `zbench`.

Install from [PyPI](https://pypi.org/project/zbench/):

```sh
pip install zbench
```


## Example

```console
$ zbench setup.cfg
path      algorithm size percentage time
setup.cfg raw_py     853   100.000% 0.000
setup.cfg gzip_py    488    57.210% 0.000
setup.cfg bz2_py     547    64.127% 0.000
setup.cfg lzma_py    572    67.057% 0.011
setup.cfg zlib_py    476    55.803% 0.000
```


## License

Copyright 2020 Christopher Brown.
[MIT Licensed](https://chbrown.github.io/licenses/MIT/#2020).
