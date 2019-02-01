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

"""Main entry point of the Mini Vouchers command line interface."""

import argparse
import logging
import sys
from typing import TextIO


from mini_vouchers.csv_utils import parse_barcodes, parse_orders
from mini_vouchers.voucher_system import VoucherSystem


def cmdline_args():
    """Define and parse command line arguments.

    Returns:
        The populated :py:class:`argparse.Namespace` from the command line
        arguments.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--barcodes",
        default="barcodes.csv",
        type=argparse.FileType("r"),
        help=(
            "List of barcodes, in a CSV file. The expected data is a set of "
            "unique `barcode`s that are optionally mapped to an `order_id`."
        ),
    )
    parser.add_argument(
        "--orders",
        default="orders.csv",
        type=argparse.FileType("r"),
        help=(
            "List of customer orders, in a CSV file. The expected data is a "
            "set of unique `order_id`s each mapped to a `customer_id`."
        ),
    )
    parser.add_argument(
        "--output",
        "-o",
        default=sys.stdout,
        type=argparse.FileType("w"),
        help="Output file to print the vouchers to.",
    )

    return parser.parse_args()


def trim_lines(text_stream: TextIO):
    """Get the trimmed lines of a text stream.

    :param file: A text stream.
    :yields: Each line read from `file` after being trimmed.

    """
    for line in text_stream:
        yield line.strip()


def main():
    """Execute the Mini Vouchers program.

    Read the dataset from the barcodes and orders files and print a list of
    vouchers per customer in the form of:

        customer_id, order_id, barcode[, barcode...]

    The lines are sorted by customer identifer and order identifier.

    """
    logging.basicConfig(level=logging.DEBUG)
    args = cmdline_args()

    exported_barcodes = parse_barcodes(trim_lines(args.barcodes))
    exported_orders = parse_orders(trim_lines(args.orders))
    system = VoucherSystem()
    system.populate(exported_barcodes, exported_orders)

    for order in system.get_orders(
        key=lambda order: (order.customer_id, order.order_id)
    ):
        # Flatten the barcodes into a comma-separated list of barcodes or into
        # an empty string.
        barcodes = ", ".join(order.barcodes)
        args.output.write(f"{order.customer_id}, {order.order_id}, {barcodes}\n")


if __name__ == "__main__":
    main()
