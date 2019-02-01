#
# Copyright 2019 Borjan Tchakaloff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""The representation and utilities to handle CSV serialisation."""

from typing import NamedTuple, Optional, Sequence


class ExportedBarcode(NamedTuple):
    """A barcode as exported in a CSV file.

    The barcode is available if the order identifier is undefined. Otherwise, it is
    assigned to that very order.
    """

    barcode: str
    """The barcode value."""
    order_id: Optional[int] = None
    """The optional order identifier."""


class ExportedOrder(NamedTuple):
    """An order as exported in a CSV file."""

    order_id: int
    """The order identifier."""
    customer_id: int
    """The customer identifier."""


def parse_barcodes(csv_input: Sequence[str]) -> Sequence[ExportedBarcode]:
    """Yield barcodes optionally assigned to orders from a CSV-like sequence.

    >>> data = parse_barcodes(["barcode,order_id", "abc,1", "def,42", "g,"])
    >>> next(data)
    ExportedBarcode(barcode='abc', order_id=1)
    >>> next(data)
    ExportedBarcode(barcode='def', order_id=42)
    >>> next(data)
    ExportedBarcode(barcode='g', order_id=None)

    The column ordering does not matter and is determined based on the first
    line (the header):

    >>> data1 = parse_barcodes(["barcode,order_id", "abcdef,123"])
    >>> data2 = parse_barcodes(["order_id,barcode", "123,abcdef"])
    >>> list(data1) == list(data2)
    True

    It is assumed that order identifiers are base 10 integers:

    >>> next(parse_barcodes(["barcode,order_id", "abc,z"]))
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: 'z'

    Lines without barcodes will be ignored:

    >>> data = parse_barcodes(["barcode,order_id", ",123"])
    >>> len(list(data))
    0

    :param:`csv_input`: The sequence of CSV-like lines to parse.
    :yields: The sequence of :py:class:`ExportedBarcode`s read.

    """
    raise NotImplementedError()


def parse_orders(csv_input: Sequence[str]) -> Sequence[ExportedOrder]:
    """Yield orders and their customers from a CSV-like sequence.

    >>> data = parse_orders(["order_id,customer_id", "1,1", "24,42"])
    >>> next(data)
    ExportedOrder(order_id=1, customer_id=1)
    >>> next(data)
    ExportedOrder(order_id=24, customer_id=42)

    The column ordering does not matter and is determined based on the first
    line:

    >>> data1 = parse_orders(["order_id,customer_id", "123,456"])
    >>> data2 = parse_orders(["customer_id,order_id", "456,123"])
    >>> list(data1) == list(data2)
    True

    It is assumed that customer and order identifiers are base 10 integers:

    >>> next(parse_orders(["order_id,customer_id", "a,0"]))
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: 'a'
    >>> next(parse_orders(["order_id,customer_id", "0,b"]))
    Traceback (most recent call last):
        ...
    ValueError: invalid literal for int() with base 10: 'b'

    Lines without both identifiers defined are ignored:

    >>> data = parse_orders(["order_id,customer_id", ",", "1,", ",1"])
    >>> len(list(data))
    0

    :param csv_input: The sequence of CSV-like lines to parse.
    :yields: The sequence of :py:class:`ExportedOrder`s read.

    """
    raise NotImplementedError()
