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

"""mini-vouchers - A minimal implementation of a voucher system.

System description
------------------

The basis of this system is the existence of a pool of barcodes that can be
ordered. Each barcode is unique. A customer can order barcodes which are then
marked as attributed and not available anymore. An order is uniquely identified
and maps barcodes to a customer.

System scope
------------

This implementation of a voucher system deals with the set of barcodes
(available and attributed) and the set of orders placed by customers.

The system is meant to create a summary of the vouchers resulting from the
orders. A voucher is the tangible artifact from a customer order and contains
the very barcodes attributed.

"""

__version__ = "0.1.0"
__author__ = "Borjan Tchakaloff <borjan@tchakaloff.fr>"
