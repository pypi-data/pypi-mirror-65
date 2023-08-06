"""
zbench CLI
"""
from fractions import Fraction
from typing import List
import logging
import os

import click

import zbench
from .formatters import Tabular
from .impl import all_impls
from .util import TimerContext

logger = logging.getLogger(zbench.__name__)


@click.command()
@click.version_option(zbench.__version__)
@click.argument("paths", type=click.Path(exists=True, dir_okay=False), nargs=-1)
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity")
def run(paths: List[str], verbose: int):
    """
    Benchmark compression ratios and speed.
    """
    level = logging.WARNING - (verbose * 10)
    logging.basicConfig(level=level)
    logging.debug("Set logging level to %s [%d]", logging.getLevelName(level), level)

    fields = ["path", "algorithm", "size", "percentage", "time"]
    formatter = Tabular(fields)
    # run paths and their sizes through formatter for the side-effects
    for path in paths:
        size = os.stat(path).st_size
        formatter.format({"path": path, "size": size})

    # print headers
    formatter.feed(dict(zip(fields, fields)))

    for path in paths:
        size = os.stat(path).st_size
        for func in all_impls:
            with TimerContext() as timer:
                compressed_size = func(path)
            report = {
                "path": path,
                "algorithm": func.__name__,
                "size": compressed_size,
                "percentage": Fraction(compressed_size, size),
                "time": timer.elapsed,
            }
            formatter.feed(report)


main = run.main

if __name__ == "__main__":
    main(prog_name=f"python -m {zbench.__name__}")
