Content divergence and trying to relocate a node on top of itself (issue5958)
https://bz.mercurial-scm.org/show_bug.cgi?id=5958

  $ . $TESTDIR/testlib/common.sh

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > rebase =
  > evolve =
  > EOF

  $ hg init issue5958
  $ cd issue5958

  $ echo hi > r0
  $ hg ci -qAm 'add r0'
  $ echo hi > foo.txt
  $ hg ci -qAm 'add foo.txt'
  $ hg metaedit -r . -d '0 2'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

(Make changes in unrelated files so that we don't have any merge conflicts
during the rebase, but the two touched revisions aren't identical)

  $ echo hi > bar.txt
  $ hg add -q bar.txt
  $ hg amend -q
  $ hg metaedit -r 1 -d '0 1' --hidden
  2 new content-divergent changesets
  $ hg log -r tip
  changeset:   4:c17bf400a278
  tag:         tip
  parent:      0:a24ed8ad918c
  user:        test
  date:        Wed Dec 31 23:59:59 1969 -0000
  instability: content-divergent
  summary:     add foo.txt
  
  $ echo hi > baz.txt
  $ hg add -q baz.txt
  $ hg amend -q
  $ hg rebase -qr tip -d 4
  $ hg log -G
  @  changeset:   6:08bc7ba82799
  |  tag:         tip
  |  parent:      4:c17bf400a278
  |  user:        test
  |  date:        Wed Dec 31 23:59:58 1969 -0000
  |  instability: content-divergent
  |  summary:     add foo.txt
  |
  *  changeset:   4:c17bf400a278
  |  parent:      0:a24ed8ad918c
  |  user:        test
  |  date:        Wed Dec 31 23:59:59 1969 -0000
  |  instability: content-divergent
  |  summary:     add foo.txt
  |
  o  changeset:   0:a24ed8ad918c
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     add r0
  
  $ hg obslog -a -r .
  @  08bc7ba82799 (6) add foo.txt
  |
  | *  c17bf400a278 (4) add foo.txt
  | |
  x |  1d1fc409af98 (5) add foo.txt
  | |    rewritten(parent, content) as 08bc7ba82799 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  a25dd7af6cf6 (3) add foo.txt
  | |    amended(content) as 1d1fc409af98 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  0065551bd38f (2) add foo.txt
  |/     amended(content) as a25dd7af6cf6 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  cc71ffbc7c00 (1) add foo.txt
       date-changed(date) as 0065551bd38f using metaedit by test (Thu Jan 01 00:00:00 1970 +0000)
       date-changed(date) as c17bf400a278 using metaedit by test (Thu Jan 01 00:00:00 1970 +0000)
  
  $ hg evolve --content-divergent
  merge:[6] add foo.txt
  with: [4] add foo.txt
  base: [1] add foo.txt
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  1 new orphan changesets
  working directory is now at 459c64f7eaad
