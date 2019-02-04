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


LOG_FORMAT = "%(asctime)s | [%(levelname)s] %(name)s: %(message)s"
LOG_LEVELS = [
    logging.NOTSET,
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
]
DEFAULT_LOG_LEVEL = logging.WARNING


def get_log_level(verbose: int, quiet: int) -> int:
    """Compute the log level.

    The log level base value is :py:const:`DEFAULT_LOG_LEVEL` and will range
    through :py:const:`LOG_LEVELS`.

    :param verbose: Number of levels to increase log level.
    :param quiet: Number of levels to decrease log level.
    :returns: The log level.
    """
    assert verbose >= 0 and quiet >= 0

    default_index = LOG_LEVELS.index(DEFAULT_LOG_LEVEL)
    index = min(len(LOG_LEVELS) - 1, max(0, default_index + quiet - verbose))

    return LOG_LEVELS[index]


def cmdline_args():
    """Define and parse command line arguments.

    Returns:
        The populated :py:class:`argparse.Namespace` from the command line
        arguments.

    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "action",
        choices=["print", "summary"],
        default="print",
        nargs="?",
        help=(
            "The action to execute. Print all vouchers in the system "
            "(`print`). Briefly describe the dataset (`summary`). Defaults to "
            "`%(default)s`."
        ),
    )

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
        help="Output file to print the vouchers to. Defaults to `stdout`.",
    )

    parser.add_argument(
        "--log",
        "-l",
        default=sys.stderr,
        type=argparse.FileType("w"),
        help="Log file. Defaults to `stderr`.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        default=0,
        action="count",
        help="Decrease log level verbosity. May be used several times.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=0,
        action="count",
        help="Increase log level verbosity. May be used several times.",
    )

    return parser.parse_args()


def trim_lines(text_stream: TextIO):
    """Get the trimmed lines of a text stream.

    :param file: A text stream.
    :yields: Each line read from `file` after being trimmed.

    """
    for line in text_stream:
        yield line.strip()


def do_print(system: VoucherSystem, output: TextIO):
    """Print all vouchers in the system.

    Print a list of vouchers per customer in the form of:

        customer_id, order_id, barcode[, barcode...]

    The lines are sorted by customer identifer and order identifier.

    :param system: The populated voucher system to print from.
    :param output: The output stream to write to.

    """
    for order in system.get_orders(
        key=lambda order: (order.customer_id, order.order_id)
    ):
        # Flatten the barcodes into a comma-separated list of barcodes or into
        # an empty string.
        barcodes = ", ".join(order.barcodes)
        output.write(f"{order.customer_id}, {order.order_id}, {barcodes}\n")


def do_summary(system: VoucherSystem, output: TextIO):
    """Briefly describe the dataset.

    Print the total amount of available barcodes, orders, barcodes, and
    customers known to the system.

    :param system: The populated voucher system to print from.
    :param output: The output stream to write to.

    """
    customers = set()
    used_barcodes = 0

    i = -1
    for i, order in enumerate(system.get_orders()):
        customers.add(order.customer_id)
        used_barcodes += len(order.barcodes)

    free_barcodes = len(system.get_available_barcodes())
    total_barcodes = used_barcodes + free_barcodes
    total_orders = i + 1
    total_customers = len(customers)

    output.write(
        f"The dataset contains {total_orders} orders from {total_customers} "
        "customers.\n"
        f"There are {free_barcodes} barcodes available out of a total of "
        f"{total_barcodes} barcodes.\n"
    )


def main():
    """Execute the Mini Vouchers program.

    Read the dataset from the barcodes and orders files, and act on the system
    based on the command line action.

    """
    args = cmdline_args()
    logging.basicConfig(
        format=LOG_FORMAT, level=get_log_level(args.verbose, args.quiet)
    )

    exported_barcodes = parse_barcodes(trim_lines(args.barcodes))
    exported_orders = parse_orders(trim_lines(args.orders))
    system = VoucherSystem()
    system.populate(exported_barcodes, exported_orders)

    if args.action == "print":
        do_print(system, args.output)
    elif args.action == "summary":
        do_summary(system, args.output)
    else:
        raise ValueError(f"Unknown action {args.action}")


if __name__ == "__main__":
    main()
