# Copyright 2010-2020 The pygit2 contributors
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2,
# as published by the Free Software Foundation.
#
# In addition to the permissions in the GNU General Public License,
# the authors give you unlimited permission to link the compiled
# version of this file into combinations with other programs,
# and to distribute those combinations without any restriction
# coming from the use of this file.  (The General Public License
# restrictions do apply in other respects; for example, they cover
# modification of the file, and distribution when not linked into
# a combined executable.)
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

"""Tests for merging and information about it."""

import os

import pytest

import pygit2
from . import utils


class CherrypickTestBasic(utils.RepoTestCaseForMerging):

    def test_cherrypick_none(self):
        with pytest.raises(TypeError): self.repo.cherrypick(None)

    def test_cherrypick_invalid_hex(self):
        branch_head_hex = '12345678'
        with pytest.raises(KeyError): self.repo.cherrypick(branch_head_hex)

    def test_cherrypick_already_something_in_index(self):
        branch_head_hex = '03490f16b15a09913edb3a067a3dc67fbb8d41f1'
        branch_oid = self.repo.get(branch_head_hex).id
        with open(os.path.join(self.repo.workdir, 'inindex.txt'), 'w') as f:
            f.write('new content')
        self.repo.index.add('inindex.txt')
        with pytest.raises(pygit2.GitError): self.repo.cherrypick(branch_oid)

class CherrypickTestWithConflicts(utils.RepoTestCaseForMerging):

    def test_cherrypick_remove_conflicts(self):
        other_branch_tip = '1b2bae55ac95a4be3f8983b86cd579226d0eb247'
        self.repo.cherrypick(other_branch_tip)
        idx = self.repo.index
        conflicts = idx.conflicts
        assert conflicts is not None
        conflicts['.gitignore']
        del idx.conflicts['.gitignore']
        with pytest.raises(KeyError): conflicts.__getitem__('.gitignore')
        assert idx.conflicts is None
