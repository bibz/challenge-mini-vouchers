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

"""The Voucher System definition."""

from typing import Callable, NamedTuple, Sequence, Set

from mini_vouchers.csv_utils import ExportedBarcode, ExportedOrder


class Order(NamedTuple):
    """A simple representation of an order."""

    order_id: int
    """The order identifier."""
    customer_id: int
    """The customer identifier."""
    barcodes: Set[str]
    """The attributed barcodes."""


class VoucherSystem:
    """The Voucher System logic.

    The Voucher System holds the different objects:

    - The pool of available barcodes (:py:meth:`get_available_barcodes`);
    - The orders placed by customers and the barcodes they were attributed
        (:py:meth:`get_orders`).

    Each order has a unique identifier, while barcodes are unique themselves.

    """

    def __init__(self):
        """Initialise the system."""
        raise NotImplementedError()

    def get_available_barcodes(self) -> Sequence[str]:
        """Get the available barcodes.

        :returns: A fresh sequence of the available barcodes, sorted by value.

        """
        raise NotImplementedError()

    def get_orders(self, key: Callable[[Order], bool] = None) -> Sequence[Order]:
        """Get the orders known to the system.

        :param key: The sorting function to apply. Defaults to sorted by value.
        :returns: A fresh sequence of the orders.

        """
        raise NotImplementedError()

    def populate(
        self,
        exported_barcodes: Sequence[ExportedBarcode],
        exported_orders: Sequence[ExportedOrder],
    ):
        """Populate the system with data previously exported.

        >>> exported_barcodes = [ExportedBarcode('a', 10), ExportedBarcode('z')]
        >>> exported_orders = [ExportedOrder(10, 7)]
        >>> system = VoucherSystem()
        >>> system.populate(exported_barcodes, exported_orders)
        >>> system.get_available_barcodes()
        ['z']
        >>> system.get_orders()
        [Order(order_id=10, customer_id=7, barcodes={'a'})]

        The data is first cleaned (duplicates are dropped) and then validated
        (bad states are dropped).

        Exported data cleaning
        ----------------------

        Order identifier unicity
        ~~~~~~~~~~~~~~~~~~~~~~~~

        Duplicate exports are ignored based on the order identifier value:

        >>> exported_barcodes = [ExportedBarcode('a', 10)]
        >>> exported_orders = [ExportedOrder(10, 7), ExportedOrder(10, 5)]
        >>> system = VoucherSystem()
        >>> system.populate(exported_barcodes, exported_orders)
        >>> system.get_orders()
        [Order(order_id=10, customer_id=7, barcodes={'a'})]

        Barcode unicity
        ~~~~~~~~~~~~~~~

        Duplicate exports are ignored based on the barcode value -- even if hold
        a different barcode attribution:

        >>> exported_barcodes = [ExportedBarcode('a'), ExportedBarcode('a', 1)]
        >>> exported_orders = []
        >>> system = VoucherSystem()
        >>> system.populate(exported_barcodes, exported_orders)
        >>> system.get_available_barcodes()
        ['a']

        Exported data validation
        ------------------------

        No empty order
        ~~~~~~~~~~~~~~

        An order must have barcodes assigned to it, it is otherwise dropped:

        >>> exported_barcodes = []
        >>> exported_orders = [ExportedOrder(10, 7)]
        >>> system = VoucherSystem()
        >>> system.populate(exported_barcodes, exported_orders)
        >>> len(system.get_orders())
        0

        :param exported_barcodes: The barcodes previously exported.
        :param exported_orders: The orders previously exported.

        """
        raise NotImplementedError()
