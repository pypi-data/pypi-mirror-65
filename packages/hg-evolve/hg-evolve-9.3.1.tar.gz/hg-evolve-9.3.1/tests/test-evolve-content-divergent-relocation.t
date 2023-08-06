======================================================
Tests the resolution of content divergence: relocation
======================================================

This file intend to cover case where changesets need to be moved to different parents

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n ({bookmarks}) [{branch}] {phase}"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH


Testing resolution of content-divergent changesets when they are on different
parents and resolution and relocation wont result in conflicts
------------------------------------------------------------------------------

  $ hg init multiparents
  $ cd multiparents
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo bar > b
  $ hg amend
  2 new orphan changesets

  $ hg rebase -r b1661037fa25 -d 8fa14d15e168 --hidden --config experimental.evolution.allowdivergence=True
  rebasing 2:b1661037fa25 "added b"
  2 new content-divergent changesets

  $ hg glog
  *  6:da4b96f4a8d6 added b
  |   () [default] draft
  | @  5:7ed0642d644b added b
  | |   () [default] draft
  | | *  4:c41c793e0ef1 added d
  | | |   () [default] draft
  | | *  3:ca1b80f7960a added c
  | | |   () [default] draft
  | | x  2:b1661037fa25 added b
  | |/    () [default] draft
  | o  1:c7586e2a9264 added a
  |/    () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[5] added b
  with: [6] added b
  base: [2] added b
  rebasing "other" content-divergent changeset da4b96f4a8d6 on c7586e2a9264
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 171614c9a791

  $ hg glog
  @  8:171614c9a791 added b
  |   () [default] draft
  | *  4:c41c793e0ef1 added d
  | |   () [default] draft
  | *  3:ca1b80f7960a added c
  | |   () [default] draft
  | x  2:b1661037fa25 added b
  |/    () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 171614c9a7914c53f531373b95632323fdbbac8d
  # Parent  c7586e2a92645e473645847a7b69a6dc52be4276
  added b
  
  diff -r c7586e2a9264 -r 171614c9a791 b
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

Resolving orphans to get back to a normal graph

  $ hg evolve --all
  move:[3] added c
  atop:[8] added b
  move:[4] added d
  $ hg glog
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  @  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

More testing!

  $ echo x > x
  $ hg ci -Aqm "added x"
  $ hg glog -r .
  @  11:71a392c714b5 added x
  |   () [default] draft
  ~

  $ echo foo > x
  $ hg branch bar
  marked working directory as branch bar
  (branches are permanent and global, did you want a bookmark?)
  $ hg amend -m "added foo to x"

  $ hg up 71a392c714b5 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 71a392c714b5
  (hidden revision '71a392c714b5' was rewritten as: 1e1a50385a7d)
  working directory parent is obsolete! (71a392c714b5)
  (use 'hg evolve' to update to its successor: 1e1a50385a7d)
  $ hg rebase -r . -d 4ae4427ee9f8 --config experimental.evolution.allowdivergence=True
  rebasing 11:71a392c714b5 "added x"
  2 new content-divergent changesets

  $ hg glog
  @  13:1e4f6b3bb39b added x
  |   () [default] draft
  | *  12:1e1a50385a7d added foo to x
  | |   () [bar] draft
  o |  10:4ae4427ee9f8 added d
  | |   () [default] draft
  o |  9:917281f93fcb added c
  |/    () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[13] added x
  with: [12] added foo to x
  base: [11] added x
  rebasing "other" content-divergent changeset 1e1a50385a7d on 4ae4427ee9f8
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at b006cf317e0e

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Branch bar
  # Node ID b006cf317e0ed16dbe786c439577475580f645f1
  # Parent  4ae4427ee9f8f0935211fd66360948b77ab5aee9
  added foo to x
  
  diff -r 4ae4427ee9f8 -r b006cf317e0e x
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/x	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +foo

The above `hg exp` and the following log call demonstrates that message, content
and branch change is preserved in case of relocation
  $ hg glog
  @  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

Testing when both the content-divergence are on different parents and resolution
will lead to conflicts
---------------------------------------------------------------------------------

  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved

  $ echo y > y
  $ hg ci -Aqm "added y"
  $ hg glog -r .
  @  16:fc6ad2bac162 added y
  |   () [default] draft
  ~

  $ echo bar > y
  $ hg amend

  $ hg up fc6ad2bac162 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset fc6ad2bac162
  (hidden revision 'fc6ad2bac162' was rewritten as: 2a9f6ccbdeba)
  working directory parent is obsolete! (fc6ad2bac162)
  (use 'hg evolve' to update to its successor: 2a9f6ccbdeba)
  $ hg rebase -r . -d b006cf317e0e --config experimental.evolution.allowdivergence=True
  rebasing 16:fc6ad2bac162 "added y"
  2 new content-divergent changesets
  $ echo wat > y
  $ hg amend

  $ hg glog
  @  19:b4575ed6fcfc added y
  |   () [bar] draft
  | *  17:2a9f6ccbdeba added y
  | |   () [default] draft
  o |  15:b006cf317e0e added foo to x
  | |   () [bar] draft
  o |  10:4ae4427ee9f8 added d
  | |   () [default] draft
  o |  9:917281f93fcb added c
  |/    () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[19] added y
  with: [17] added y
  base: [16] added y
  rebasing "other" content-divergent changeset 2a9f6ccbdeba on b006cf317e0e
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [1]

  $ echo watbar > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 7bbcf24ddecf

  $ hg glog
  @  21:7bbcf24ddecf added y
  |   () [bar] draft
  o  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg obslog -r . --all
  @    7bbcf24ddecf (21) added y
  |\
  x |  48f745db3f53 (20) added y
  | |    rewritten(branch, content) as 7bbcf24ddecf using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  b4575ed6fcfc (19) added y
  | |    amended(content) as 7bbcf24ddecf using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  2a9f6ccbdeba (17) added y
  | |    rebased(parent) as 48f745db3f53 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  96b677f01b81 (18) added y
  |/     amended(content) as b4575ed6fcfc using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  fc6ad2bac162 (16) added y
       amended(content) as 2a9f6ccbdeba using amend by test (Thu Jan 01 00:00:00 1970 +0000)
       rewritten(branch, parent) as 96b677f01b81 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  

checking that relocated commit is there
  $ hg exp 48f745db3f53 --hidden
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 48f745db3f5300363ca248b9aeab20ff2a55fbb3
  # Parent  b006cf317e0ed16dbe786c439577475580f645f1
  added y
  
  diff -r b006cf317e0e -r 48f745db3f53 y
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

Testing when the relocation will result in conflicts and merging also:
----------------------------------------------------------------------

  $ hg glog
  @  21:7bbcf24ddecf added y
  |   () [bar] draft
  o  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up .^^^^
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved

  $ echo z > z
  $ hg ci -Aqm "added z"
  $ hg glog -r .
  @  22:daf1de08f3b0 added z
  |   () [default] draft
  ~

  $ echo foo > y
  $ hg add y
  $ hg amend

  $ hg up daf1de08f3b0 --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset daf1de08f3b0
  (hidden revision 'daf1de08f3b0' was rewritten as: 3f7a1f693080)
  working directory parent is obsolete! (daf1de08f3b0)
  (use 'hg evolve' to update to its successor: 3f7a1f693080)
  $ hg rebase -r . -d 7bbcf24ddecf --config experimental.evolution.allowdivergence=True
  rebasing 22:daf1de08f3b0 "added z"
  2 new content-divergent changesets
  $ echo bar > z
  $ hg amend

  $ hg glog
  @  25:53242575ffa9 added z
  |   () [bar] draft
  | *  23:3f7a1f693080 added z
  | |   () [default] draft
  o |  21:7bbcf24ddecf added y
  | |   () [bar] draft
  o |  15:b006cf317e0e added foo to x
  | |   () [bar] draft
  o |  10:4ae4427ee9f8 added d
  | |   () [default] draft
  o |  9:917281f93fcb added c
  |/    () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent --any
  merge:[25] added z
  with: [23] added z
  base: [22] added z
  rebasing "other" content-divergent changeset 3f7a1f693080 on 7bbcf24ddecf
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [1]

  $ hg diff
  diff -r 7bbcf24ddecf y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 7bbcf24ddecf bar - test: added y
   watbar
  +=======
  +foo
  +>>>>>>> evolving:    3f7a1f693080 - test: added z
  diff -r 7bbcf24ddecf z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +z

  $ echo foo > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 23:3f7a1f693080 "added z"
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  unresolved merge conflicts
  (see 'hg help evolve.interrupted')
  [1]

  $ hg diff
  diff -r 53242575ffa9 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< local: 53242575ffa9 bar - test: added z
   watbar
  +=======
  +foo
  +>>>>>>> other: cdb0643c69fc - test: added z

  $ echo foo > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 6fc7d9682de6

  $ hg glog
  @  27:6fc7d9682de6 added z
  |   () [bar] draft
  o  21:7bbcf24ddecf added y
  |   () [bar] draft
  o  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Branch bar
  # Node ID 6fc7d9682de6e3bee6c8b1266b756ed7d522b7e4
  # Parent  7bbcf24ddecfe97d7c2ac6fa8c07c155c8fda47b
  added z
  
  diff -r 7bbcf24ddecf -r 6fc7d9682de6 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -watbar
  +foo
  diff -r 7bbcf24ddecf -r 6fc7d9682de6 z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

  $ cd ..
