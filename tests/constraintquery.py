# Copyright 2015, Tresys Technology, LLC
#
# This file is part of SETools.
#
# SETools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# SETools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SETools.  If not, see <http://www.gnu.org/licenses/>.
#
import unittest

from setools import SELinuxPolicy
from setools.constraintquery import ConstraintQuery


class ConstraintQueryTest(unittest.TestCase):

    def setUp(self):
        self.p = SELinuxPolicy("tests/constraintquery.conf")

    def test_000_unset(self):
        """Constraint query with no criteria."""
        allconstraint = sorted(c.tclass for c in self.p.constraints())

        q = ConstraintQuery(self.p)
        qconstraint = sorted(c.tclass for c in q.results())

        self.assertListEqual(allconstraint, qconstraint)

    def test_001_ruletype(self):
        """Constraint query with rule type match."""
        q = ConstraintQuery(self.p, ruletype=["mlsconstrain"])

        constraint = sorted(c.tclass for c in q.results())
        self.assertListEqual(["test1"], constraint)

    def test_010_class_exact(self):
        """Constraint query with exact object class match."""
        q = ConstraintQuery(self.p, tclass="test10")

        constraint = sorted(c.tclass for c in q.results())
        self.assertListEqual(["test10"], constraint)

    def test_011_class_list(self):
        """Constraint query with object class list match."""
        q = ConstraintQuery(self.p, tclass=["test11a", "test11b"])

        constraint = sorted(c.tclass for c in q.results())
        self.assertListEqual(["test11a", "test11b"], constraint)

    def test_012_class_list(self):
        """Constraint query with object class list match."""
        q = ConstraintQuery(self.p, tclass="test12(a|c)", tclass_regex=True)

        constraint = sorted(c.tclass for c in q.results())
        self.assertListEqual(["test12a", "test12c"], constraint)

    def test_020_perms_any(self):
        """Constraint query with permission set intersection match."""
        q = ConstraintQuery(self.p, perms=["test20ap", "test20bp"])

        constraint = sorted(c.tclass for c in q.results())
        self.assertListEqual(["test20a", "test20b"], constraint)

    def test_020_perms_equal(self):
        """Constraint query with permission set equality match."""
        q = ConstraintQuery(self.p, perms=["test21ap", "test21bp"], perms_equal=True)

        constraint = sorted(c.tclass for c in q.results())
        self.assertListEqual(["test21c"], constraint)
