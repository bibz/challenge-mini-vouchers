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

from collections import Counter
import logging
from typing import Any, Callable, Dict, NamedTuple, Optional, Sequence, Set, Tuple

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

    _all_barcodes: Dict[str, Optional[int]]
    """The pool of available barcodes mapped to their order identifier."""
    _orders: Dict[int, Order]
    """The orders addressed by their identifier."""

    def __init__(self):
        """Initialise the system."""
        self._all_barcodes = {}
        self._orders = {}

    def get_available_barcodes(self) -> Sequence[str]:
        """Get the available barcodes.

        :returns: A fresh sequence of the available barcodes, sorted by value.

        """
        return sorted(
            filter(
                lambda barcode: not self._all_barcodes[barcode],
                self._all_barcodes.keys(),
            )
        )

    def get_orders(self, key: Callable[[Order], Any] = None) -> Sequence[Order]:
        """Get the orders known to the system.

        :param key: The sorting function to apply. Defaults to sorted by value.
        :returns: A fresh sequence of the orders.

        """
        return sorted(self._orders.values(), key=key)

    def get_top_customers(self, limit: int) -> Sequence[Tuple[int, int]]:
        """Get the top customers.

        Compute and yield the top customers based on how many barcodes they
        ordered.

        >>> # Begin the range at 1 to avoid empty barcodes.
        >>> exported_barcodes = [ExportedBarcode('a'*i, 100+i) for i in range(1,5)]
        >>> exported_barcodes += [ExportedBarcode('b'*i, 200+i) for i in range(1,20)]
        >>> exported_barcodes += [ExportedBarcode('c'*i, 300+i) for i in range(1,10)]
        >>> exported_orders = [ExportedOrder(100+i, 33) for i in range(1,5)]
        >>> exported_orders += [ExportedOrder(200+i, 44) for i in range(1,20)]
        >>> exported_orders += [ExportedOrder(300+i, 55) for i in range(1,10)]
        >>> system = VoucherSystem()
        >>> system.populate(exported_barcodes, exported_orders)
        >>> system.get_top_customers(2)
        [(44, 19), (55, 9)]

        :param limit: The amount of top customers to return.
        :returns: A fresh sequence of tuples of customer identifier and their
            amount of barcodes, ranked from high (most barcodes) to low.

        """
        assert limit >= 0

        customer_total_barcodes: Counter = Counter()

        for order in self.get_orders():
            customer_total_barcodes.update({order.customer_id: len(order.barcodes)})

        return customer_total_barcodes.most_common()[:limit]

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
        (bad states are dropped):

        #.  Duplicate **order** exports are ignored based on the order
            identifier value:

            >>> exported_barcodes = [ExportedBarcode('a', 10)]
            >>> exported_orders = [ExportedOrder(10, 7), ExportedOrder(10, 5)]
            >>> system = VoucherSystem()
            >>> system.populate(exported_barcodes, exported_orders)
            >>> system.get_orders()
            [Order(order_id=10, customer_id=7, barcodes={'a'})]

        #.  Duplicate **barcode** exports are ignored based on the barcode
            value -- even if they hold a different barcode attribution:

            >>> exported_barcodes = [ExportedBarcode('a'), ExportedBarcode('a', 1)]
            >>> exported_orders = []
            >>> system = VoucherSystem()
            >>> system.populate(exported_barcodes, exported_orders)
            >>> system.get_available_barcodes()
            ['a']

        #.  An order must have barcodes assigned to it, it is otherwise dropped:

            >>> exported_barcodes = []
            >>> exported_orders = [ExportedOrder(10, 7)]
            >>> system = VoucherSystem()
            >>> system.populate(exported_barcodes, exported_orders)
            >>> len(system.get_orders())
            0

        :param exported_barcodes: The barcodes previously exported.
        :param exported_orders: The orders previously exported.

        """
        # Populate the orders
        for exported_order in exported_orders:
            order_id, customer_id = exported_order

            if order_id not in self._orders:
                logging.debug("Adding new order %s", exported_order)
                self._orders[order_id] = Order(order_id, customer_id, set())
            else:
                logging.warning("Discarding duplicate order %s", exported_order)

        # Populate the barcodes
        for exported_barcode in exported_barcodes:
            barcode, opt_order_id = exported_barcode

            if barcode in self._all_barcodes:
                logging.warning("Discarding duplicate barcode %s", exported_barcode)
                continue

            logging.debug("Adding new barcode %s", exported_barcode)
            self._all_barcodes[barcode] = opt_order_id

            if opt_order_id and opt_order_id in self._orders:
                self._orders[opt_order_id].barcodes.add(barcode)
            elif opt_order_id:
                logging.warning(
                    "Discarding barcode %s from unknown order", exported_barcode
                )

        # Validate the orders
        for order in list(self._orders.values()):
            if not order.barcodes:
                logging.warning("Discarding order without barcodes %s", order)
                self._orders.pop(order.order_id)
