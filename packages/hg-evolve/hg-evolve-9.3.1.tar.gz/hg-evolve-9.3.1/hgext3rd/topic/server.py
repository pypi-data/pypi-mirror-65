# topic/server.py - server specific behavior with topic
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
from mercurial import (
    extensions,
    repoview,
    wireprototypes,
    wireprotov1peer,
    wireprotov1server,
)


try:
    from mercurial.utils import (
        repoviewutil,
    )
    repoviewutil.subsettable
except (AttributeError, ImportError):
    # hg <= 4.8
    from mercurial import branchmap as repoviewutil

from . import (
    common,
    constants,
)

### Visibility restriction
#
# Serving draft changesets with topics to clients without topic extension can
# confuse them, because they won't see the topic label and will consider them
# normal anonymous heads. Instead we have the option to not serve changesets
# with topics to clients without topic support.
#
# To achieve this, we alter the behavior of the standard `heads` commands and
# introduce a new `heads` command that only clients with topic will know about.

# compat version of the wireprotocommand decorator, taken from evolve compat

FILTERNAME = b'served-no-topic'

def computeunservedtopic(repo, visibilityexceptions=None):
    assert not repo.changelog.filteredrevs
    filteredrevs = repoview.filtertable[b'served'](repo, visibilityexceptions).copy()
    mutable = repoview.filtertable[b'immutable'](repo, visibilityexceptions)
    consider = mutable - filteredrevs
    cl = repo.changelog
    extrafiltered = set()
    for r in consider:
        if cl.changelogrevision(r).extra.get(constants.extrakey, b''):
            extrafiltered.add(r)
    if extrafiltered:
        extrafiltered = set(repo.revs('%ld::%ld', extrafiltered, consider))
        filteredrevs = frozenset(filteredrevs | extrafiltered)
    return filteredrevs

def wireprotocommand(name, args=b'', permission=b'pull'):
    try:
        from mercurial.wireprotov1server import wireprotocommand
    except (ImportError, AttributeError):
        # hg <= 4.6 (b4d85bc122bd)
        from mercurial.wireproto import wireprotocommand
    return wireprotocommand(name, args, permission=permission)

def wrapheads(orig, repo, proto):
    """wrap head to hide topic^W draft changeset to old client"""
    hidetopics = repo.ui.configbool(b'experimental', b'topic.server-gate-topic-changesets')
    if common.hastopicext(repo) and hidetopics:
        h = repo.filtered(FILTERNAME).heads()
        return wireprototypes.bytesresponse(wireprototypes.encodelist(h) + b'\n')
    return orig(repo, proto)

def topicheads(repo, proto):
    """Same as the normal wireprotocol command, but accessing with a different end point."""
    h = repo.heads()
    return wireprototypes.bytesresponse(wireprototypes.encodelist(h) + b'\n')

def wireprotocaps(orig, repo, proto):
    """advertise the new topic specific `head` command for client with topic"""
    caps = orig(repo, proto)
    if common.hastopicext(repo) and repo.peer().capable(b'topics'):
        caps.append(b'_exttopics_heads')
    return caps

def setupserver(ui):
    extensions.wrapfunction(wireprotov1server, 'heads', wrapheads)
    wireprotov1server.commands.pop(b'heads')
    wireprotocommand(b'heads', permission=b'pull')(wireprotov1server.heads)
    wireprotocommand(b'_exttopics_heads', permission=b'pull')(topicheads)
    extensions.wrapfunction(wireprotov1server, '_capabilities', wireprotocaps)

    class topicpeerexecutor(wireprotov1peer.peerexecutor):

        def callcommand(self, command, args):
            if command == b'heads':
                if self._peer.capable(b'_exttopics_heads'):
                    command = b'_exttopics_heads'
                    if getattr(self._peer, '_exttopics_heads', None) is None:
                        self._peer._exttopics_heads = self._peer.heads
            s = super(topicpeerexecutor, self)
            return s.callcommand(command, args)

    wireprotov1peer.peerexecutor = topicpeerexecutor

    if FILTERNAME not in repoview.filtertable:
        repoview.filtertable[FILTERNAME] = computeunservedtopic
        repoviewutil.subsettable[FILTERNAME] = b'immutable'
        repoviewutil.subsettable[b'served'] = FILTERNAME
