# Derived from portconquery.py
#
# This file is part of SETools.
#
# SETools is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 2.1 of
# the License, or (at your option) any later version.
#
# SETools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SETools.  If not, see
# <http://www.gnu.org/licenses/>.
#
import logging

from . import contextquery
from .policyrep.xencontext import device_id

class PcideviceconQuery(contextquery.ContextQuery):

    """
    Pcidevicecon context query.

    Parameter:
    policy          The policy to query.

    Keyword Parameters/Class attributes:
    device           A single PCI device ID.

    user            The criteria to match the context's user.
    user_regex      If true, regular expression matching
                    will be used on the user.

    role            The criteria to match the context's role.
    role_regex      If true, regular expression matching
                    will be used on the role.

    type_           The criteria to match the context's type.
    type_regex      If true, regular expression matching
                    will be used on the type.

    range_          The criteria to match the context's range.
    range_subset    If true, the criteria will match if it is a subset
                    of the context's range.
    range_overlap   If true, the criteria will match if it overlaps
                    any of the context's range.
    range_superset  If true, the criteria will match if it is a superset
                    of the context's range.
    range_proper    If true, use proper superset/subset operations.
                    No effect if not using set operations.
    """

    _device = None


    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        pending_device = device_id(*value)

        if all(pending_device):
            if pending_device.low < 1:
                raise ValueError("PCI device ID must be positive: {0}".format(pending_device))

            self._device = pending_device
        else:
            self._device = None

    def results(self):
        """Generator which yields all matching pcidevicecons."""
        self.log.info("Generating results from {0.policy}".format(self))
        self.log.debug("device id: {0.device}".format(self))
        self.log.debug("User: {0.user!r}, regex: {0.user_regex}".format(self))
        self.log.debug("Role: {0.role!r}, regex: {0.role_regex}".format(self))
        self.log.debug("Type: {0.type_!r}, regex: {0.type_regex}".format(self))
        self.log.debug("Range: {0.range_!r}, subset: {0.range_subset}, overlap: {0.range_overlap}, "
                       "superset: {0.range_superset}, proper: {0.range_proper}".format(self))

        for pcidevicecon in self.policy.pcidevicecons():

            if self.device and self.device != pcidevicecon.device:
                continue

            if not self._match_context(pcidevicecon.context):
                continue
            yield pcidevicecon
