# Copyright 2014-2015, Tresys Technology, LLC
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

from . import compquery
from . import contextquery


class InitialSIDQuery(compquery.ComponentQuery, contextquery.ContextQuery):

    """
    Initial SID (Initial context) query.

    Parameter:
    policy            The policy to query.

    Keyword Parameters/Class attributes:
    name            The Initial SID name to match.
    name_regex      If true, regular expression matching
                    will be used on the Initial SID name.
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

    def __init__(self, policy, **kwargs):
        super(InitialSIDQuery, self).__init__(policy, **kwargs)
        self.log = logging.getLogger(__name__)

    def results(self):
        """Generator which yields all matching initial SIDs."""
        self.log.info("Generating initial SID results from {0.policy}".format(self))
        self.log.debug("Name: {0.name!r}, regex: {0.name_regex}".format(self))
        self.log.debug("User: {0.user!r}, regex: {0.user_regex}".format(self))
        self.log.debug("Role: {0.role!r}, regex: {0.role_regex}".format(self))
        self.log.debug("Type: {0.type_!r}, regex: {0.type_regex}".format(self))
        self.log.debug("Range: {0.range_!r}, subset: {0.range_subset}, overlap: {0.range_overlap}, "
                       "superset: {0.range_superset}, proper: {0.range_proper}".format(self))

        for i in self.policy.initialsids():
            if not self._match_name(i):
                continue

            if not self._match_context(i.context):
                continue

            yield i
