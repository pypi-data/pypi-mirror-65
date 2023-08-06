# Copyright 2011 Peter Arrenbrecht <peter.arrenbrecht@gmail.com>
#                Logilab SA        <contact@logilab.fr>
#                Pierre-Yves David <pierre-yves.david@ens-lyon.org>
#                Patrick Mezard <patrick@mezard.eu>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""evolve templates
"""

from . import (
    error,
    exthelper,
)

from mercurial import (
    templatekw,
    util
)

eh = exthelper.exthelper()

### template keywords

if util.safehasattr(templatekw, 'compatlist'):
    @eh.templatekeyword(b'instabilities', requires={b'ctx', b'templ'})
    def showinstabilities(context, mapping):
        """List of strings. Evolution instabilities affecting the changeset
        (zero or more of "orphan", "content-divergent" or "phase-divergent")."""
        ctx = context.resource(mapping, b'ctx')
        return templatekw.compatlist(context, mapping, b'instability',
                                     ctx.instabilities(),
                                     plural=b'instabilities')

    @eh.templatekeyword(b'troubles', requires={b'ctx', b'templ'})
    def showtroubles(context, mapping):   # legacy name for instabilities
        ctx = context.resource(mapping, b'ctx')
        return templatekw.compatlist(context, mapping, b'trouble',
                                     ctx.instabilities(), plural=b'troubles')
else:
    # older template API in hg < 4.6
    @eh.templatekeyword(b'instabilities')
    def showinstabilities(**args):
        """List of strings. Evolution instabilities affecting the changeset
        (zero or more of "orphan", "content-divergent" or "phase-divergent")."""
        ctx = args[b'ctx']
        return templatekw.showlist(b'instability', ctx.instabilities(), args,
                                   plural=b'instabilities')

    @eh.templatekeyword(b'troubles')
    def showtroubles(**args):
        ctx = args[b'ctx']
        return templatekw.showlist(b'trouble', ctx.instabilities(), args,
                                   plural=b'troubles')

_sp = templatekw.showpredecessors
if util.safehasattr(_sp, '_requires'):
    def showprecursors(context, mapping):
        return _sp(context, mapping)
    showprecursors.__doc__ = _sp._origdoc
    _tk = templatekw.templatekeyword(b"precursors", requires=_sp._requires)
    _tk(showprecursors)
else:
    templatekw.keywords[b"precursors"] = _sp


def closestsuccessors(repo, nodeid):
    """ returns the closest visible successors sets instead.
    """
    return directsuccessorssets(repo, nodeid)

_ss = templatekw.showsuccessorssets
if util.safehasattr(_ss, '_requires'):
    def showsuccessors(context, mapping):
        return _ss(context, mapping)
    showsuccessors.__doc__ = _ss._origdoc
    _tk = templatekw.templatekeyword(b"successors", requires=_ss._requires)
    _tk(showsuccessors)
else:
    templatekw.keywords[b"successors"] = _ss

def _getusername(ui):
    """the default username in the config or None"""
    try:
        return ui.username()
    except error.Abort: # no easy way to avoid ui raising Abort here :-/
        return None

# copy from mercurial.obsolete with a small change to stop at first known changeset.

def directsuccessorssets(repo, initialnode, cache=None):
    """return set of all direct successors of initial nodes
    """

    succmarkers = repo.obsstore.successors

    # Stack of nodes we search successors sets for
    toproceed = [initialnode]
    # set version of above list for fast loop detection
    # element added to "toproceed" must be added here
    stackedset = set(toproceed)

    pathscache = {}

    if cache is None:
        cache = {}
    while toproceed:
        current = toproceed[-1]
        if current in cache:
            stackedset.remove(toproceed.pop())
        elif current != initialnode and current in repo:
            # We have a valid direct successors.
            cache[current] = [(current,)]
        elif current not in succmarkers:
            if current in repo:
                # We have a valid last successors.
                cache[current] = [(current,)]
            else:
                # Final obsolete version is unknown locally.
                # Do not count that as a valid successors
                cache[current] = []
        else:
            for mark in sorted(succmarkers[current]):
                for suc in mark[1]:
                    if suc not in cache:
                        if suc in stackedset:
                            # cycle breaking
                            cache[suc] = []
                        else:
                            # case (3) If we have not computed successors sets
                            # of one of those successors we add it to the
                            # `toproceed` stack and stop all work for this
                            # iteration.
                            pathscache.setdefault(suc, []).append((current, mark))
                            toproceed.append(suc)
                            stackedset.add(suc)
                            break
                else:
                    continue
                break
            else:
                succssets = []
                for mark in sorted(succmarkers[current]):
                    # successors sets contributed by this marker
                    markss = [[]]
                    for suc in mark[1]:
                        # cardinal product with previous successors
                        productresult = []
                        for prefix in markss:
                            for suffix in cache[suc]:
                                newss = list(prefix)
                                for part in suffix:
                                    # do not duplicated entry in successors set
                                    # first entry wins.
                                    if part not in newss:
                                        newss.append(part)
                                productresult.append(newss)
                        markss = productresult
                    succssets.extend(markss)
                # remove duplicated and subset
                seen = []
                final = []
                candidate = sorted(((set(s), s) for s in succssets if s),
                                   key=lambda x: len(x[1]), reverse=True)
                for setversion, listversion in candidate:
                    for seenset in seen:
                        if setversion.issubset(seenset):
                            break
                    else:
                        final.append(listversion)
                        seen.append(setversion)
                final.reverse() # put small successors set first
                cache[current] = final

    return cache[initialnode], pathscache
