from fractions import Fraction
from numbers import Number
from typing import Any, Iterable, List


def _format(value: Any) -> str:
    if value is None:
        return "␀"
    if isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, Fraction):
        return f"{float(value):.3%}"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def _formatjust(value: Any, width: int) -> str:
    """
    Render `value` into a string of length `width`, right-justified for numbers,
    otherwise left-justified.
    """
    string = _format(value)
    if isinstance(value, Number):
        return string.rjust(width)
    return string.ljust(width)


class Column:
    # pylint: disable=too-few-public-methods
    name: str
    width: int

    def __init__(self, name: str):
        self.name = name
        self.width = len(name)

    def format(self, value: Any) -> str:
        """
        Format `value` to fill this column, expanding if needed.
        """
        cell = _formatjust(value, self.width)
        cell_width = len(cell)
        if cell_width > self.width:
            self.width = cell_width
        return cell


class Tabular:
    """
    Format into whitespace-separated columns.
    """

    columns: List[Column]

    def __init__(self, names: Iterable[str] = ()):
        self.columns = []
        for name in names:
            self._add_column(name)

    def _add_column(self, name: str):
        column = Column(name)
        self.columns.append(column)

    def format(self, record: dict, sep: str = " ") -> str:
        """
        Generate string representing `record`, adding and expanding columns as needed.
        """
        column_names = [column.name for column in self.columns]
        new_column_names = set(record) - set(column_names)
        if new_column_names:
            # iterate in natural order since set() is not ordered
            for key in record:
                if key in new_column_names:
                    self._add_column(key)

        return sep.join(
            column.format(record.get(column.name)) for column in self.columns
        )

    def feed(self, record: dict, sep: str = " "):
        """
        Format `record` and print to stdout.
        """
        print(self.format(record, sep), flush=True)
