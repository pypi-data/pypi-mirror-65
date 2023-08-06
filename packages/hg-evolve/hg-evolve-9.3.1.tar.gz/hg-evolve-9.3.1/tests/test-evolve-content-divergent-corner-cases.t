========================================================
Tests the resolution of content divergence: corner cases
========================================================

This file intend to cover cases that are specific enough to not fit in the
other cases.

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n ({bookmarks}) [{branch}] {phase}"
  > [defaults]
  > amend=-d "0 0"
  > fold=-d "0 0"
  > [web]
  > push_ssl = false
  > allow_push = *
  > [phases]
  > publish = False
  > [diff]
  > git = 1
  > unified = 0
  > [ui]
  > logtemplate = {rev}:{node|short}@{branch}({phase}) {desc|firstline} [{instabilities}]\n
  > [experimental]
  > evolution.allowdivergence = True
  > [extensions]
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH
  $ mkcommit() {
  >    echo "$1" > "$1"
  >    hg add "$1"
  >    hg ci -m "add $1"
  > }

  $ mkcommits() {
  >   for i in $@; do mkcommit $i ; done
  > }

Basic test of divergence: two divergent changesets with the same parents
With --all --any we dedupe the divergent and solve the divergence once

  $ hg init test1
  $ cd test1
  $ echo a > a
  $ hg ci -Aqm "added a"
  $ echo b > b
  $ hg ci -Aqm "added b"

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent1
  $ hg ci -Am "divergent"
  adding bdivergent1
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent2
  $ hg ci -Am "divergent"
  adding bdivergent2
  created new head

  $ hg prune -s 8374d2ddc3a4 "desc('added b')"
  1 changesets pruned
  $ hg prune -s 593c57f2117e "desc('added b')" --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg log -G
  @  3:8374d2ddc3a4@default(draft) divergent [content-divergent]
  |
  | *  2:593c57f2117e@default(draft) divergent [content-divergent]
  |/
  o  0:9092f1db7931@default(draft) added a []
  

  $ hg evolve --all --any --content-divergent --update
  merge:[2] divergent
  with: [3] divergent
  base: [1] added b
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 45bf1312f454
  $ hg log -G
  @  4:45bf1312f454@default(draft) divergent []
  |
  o  0:9092f1db7931@default(draft) added a []
  
Test divergence resolution when it yields to an empty commit (issue4950)
cdivergent2 contains the same content than cdivergent1 and they are divergent
versions of the revision _c

  $ hg up .^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ mkcommit _c
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit cdivergent1
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo "cdivergent1" > cdivergent1
  $ hg add cdivergent1
  $ hg ci -m "add _c"
  created new head

  $ hg log -G
  @  7:b2ae71172042@default(draft) add _c []
  |
  | o  6:e3ff64ce8d4c@default(draft) add cdivergent1 []
  |/
  | o  5:48819a835615@default(draft) add _c []
  |/
  | o  4:45bf1312f454@default(draft) divergent []
  |/
  o  0:9092f1db7931@default(draft) added a []
  

  $ hg prune -s b2ae71172042 48819a835615
  1 changesets pruned
  $ hg prune -s e3ff64ce8d4c 48819a835615 --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg log -G
  @  7:b2ae71172042@default(draft) add _c [content-divergent]
  |
  | *  6:e3ff64ce8d4c@default(draft) add cdivergent1 [content-divergent]
  |/
  | o  4:45bf1312f454@default(draft) divergent []
  |/
  o  0:9092f1db7931@default(draft) added a []
  
  $ hg evolve --all --any --content-divergent
  merge:[6] add cdivergent1
  with: [7] add _c
  base: [5] add _c
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  nothing changed
  working directory is now at e3ff64ce8d4c

  $ cd ..

Test None docstring issue of evolve divergent, which caused hg crush

  $ hg init test2
  $ cd test2
  $ mkcommits _a _b

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent11
  $ hg ci -Am "bdivergent"
  adding bdivergent11
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent22
  $ hg ci -Am "bdivergent"
  adding bdivergent22
  created new head

  $ hg log -G
  @  3:6b096fb45070@default(draft) bdivergent []
  |
  | o  2:05a6b6a9e633@default(draft) bdivergent []
  |/
  | o  1:37445b16603b@default(draft) add _b []
  |/
  o  0:135f39f4bd78@default(draft) add _a []
  

  $ hg prune -s 6b096fb45070 37445b16603b
  1 changesets pruned
  $ hg prune -s 05a6b6a9e633 37445b16603b --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg log -G
  @  3:6b096fb45070@default(draft) bdivergent [content-divergent]
  |
  | *  2:05a6b6a9e633@default(draft) bdivergent [content-divergent]
  |/
  o  0:135f39f4bd78@default(draft) add _a []
  

  $ cat >$TESTTMP/test_extension.py  << EOF
  > from mercurial import merge
  > origupdate = merge.update
  > def newupdate(*args, **kwargs):
  >   return origupdate(*args, **kwargs)
  > merge.update = newupdate
  > EOF
  $ cat >> $HGRCPATH << EOF
  > [extensions]
  > testextension=$TESTTMP/test_extension.py
  > EOF
  $ hg evolve
  nothing to evolve on current working copy parent
  (do you want to use --content-divergent)
  [2]
  $ hg evolve --content-divergent
  merge:[2] bdivergent
  with: [3] bdivergent
  base: [1] add _b
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 73ff357d3975

  $ cd ..

Test to make sure that evolve don't fall into unrecoverable state (issue6053)
------------------------------------------------------------------------------

It happened when two divergent csets has different parent (need relocation)
and resolution parent is obsolete. So this issue triggered when during
relocation we hit conflicts. So lets make the repo as described.

  $ hg init localside
  $ cd localside
  $ for ch in a b c d e; do
  > echo $ch > $ch;
  > hg add $ch;
  > hg ci -m "added "$ch;
  > done;

  $ hg glog
  @  4:8d71eadcc9df added e
  |   () [default] draft
  o  3:9150fe93bec6 added d
  |   () [default] draft
  o  2:155349b645be added c
  |   () [default] draft
  o  1:5f6d8a4bf34a added b
  |   () [default] draft
  o  0:9092f1db7931 added a
      () [default] draft

  $ echo ee > e
  $ hg amend -m "updated e"
  $ hg up 1 -q

To make sure we hit conflict while relocating
  $ echo dd > d
  $ echo ee > e
  $ hg add d e
  $ hg ci -m "updated e"
  created new head

Lets create divergence
  $ hg prune 4 -s . --hidden
  1 changesets pruned
  2 new content-divergent changesets

Making obsolete resolution parent
  $ hg prune 3
  1 changesets pruned
  1 new orphan changesets

  $ hg glog
  @  6:de4ea3103326 updated e
  |   () [default] draft
  | *  5:ff6f7cd76a7c updated e
  | |   () [default] draft
  | x  3:9150fe93bec6 added d
  | |   () [default] draft
  | o  2:155349b645be added c
  |/    () [default] draft
  o  1:5f6d8a4bf34a added b
  |   () [default] draft
  o  0:9092f1db7931 added a
      () [default] draft

  $ hg evolve --content-divergent --any --update --config ui.interactive=true <<EOF
  > c
  > EOF
  merge:[5] updated e
  with: [6] updated e
  base: [4] added e
  rebasing "divergent" content-divergent changeset ff6f7cd76a7c on 155349b645be
  rebasing "other" content-divergent changeset de4ea3103326 on 155349b645be
  file 'd' was deleted in local but was modified in other.
  You can use (c)hanged version, leave (d)eleted, or leave (u)nresolved.
  What do you want to do? c
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  working directory is now at eb6357cd41b6

  $ hg glog -l1
  @  9:eb6357cd41b6 updated e
  |   () [default] draft
  ~

  $ cd ..

Check that canceling of file deletion are merge correctly
---------------------------------------------------------

File addition/deletion tend to have special processing. So we better test them directory

  $ hg init non-public
  $ cd non-public
  $ echo a > a
  $ echo b > b
  $ echo c > c
  $ echo d > d
  $ hg ci -Aqm initial

oops, we meant to delete just 'a', but we deleted 'b' and 'c' too

  $ hg rm a b c
  $ hg ci -m 'delete a'
  $ hg revert -r .^ b
  $ hg amend

create some content divergence

  $ hg co dff6e52f5e41 --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset dff6e52f5e41
  (hidden revision 'dff6e52f5e41' was rewritten as: 0825dcee2670)
  working directory parent is obsolete! (dff6e52f5e41)
  (use 'hg evolve' to update to its successor: 0825dcee2670)
  $ hg revert -r .^ c
  $ hg amend
  2 new content-divergent changesets
  $ hg glog --hidden
  @  3:92ecd58f9b05 delete a
  |   () [default] draft
  | *  2:0825dcee2670 delete a
  |/    () [default] draft
  | x  1:dff6e52f5e41 delete a
  |/    () [default] draft
  o  0:75d2b02c4a5c initial
      () [default] draft

Resolve the divergence, only "a" should be removed

  $ hg evolve --content-divergent --update
  merge:[2] delete a
  with: [3] delete a
  base: [1] delete a
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 7ca6a9fafcf6
  $ hg glog
  @  4:7ca6a9fafcf6 delete a
  |   () [default] draft
  o  0:75d2b02c4a5c initial
      () [default] draft

  $ hg diff --change .
  diff --git a/a b/a
  deleted file mode 100644
  --- a/a
  +++ /dev/null
  @@ -1,1 +0,0 @@
  -a
