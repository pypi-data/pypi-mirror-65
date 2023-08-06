# Copyright 2017 FUJIWARA Katsunori <foozy@lares.dti.ne.jp>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""
Compatibility module
"""
from __future__ import absolute_import

from mercurial import (
    pycompat,
    registrar,
    util,
)

if pycompat.ispy3:
    def branchmapitems(branchmap):
        return branchmap.items()
else:
    # py3-transform: off
    def branchmapitems(branchmap):
        return branchmap.iteritems()
    # py3-transform: on

# help category compatibility
# hg <= 4.7 (c303d65d2e34)
def helpcategorykwargs(categoryname):
    """Backwards-compatible specification of the helpategory argument."""
    category = getattr(registrar.command, categoryname, None)
    if not category:
        return {}
    return {'helpcategory': category}

# nodemap.get and index.[has_node|rev|get_rev]
# hg <= 5.3 (02802fa87b74)
def getgetrev(cl):
    """Returns index.get_rev or nodemap.get (for pre-5.3 Mercurial)."""
    if util.safehasattr(cl.index, 'get_rev'):
        return cl.index.get_rev
    return cl.nodemap.get
