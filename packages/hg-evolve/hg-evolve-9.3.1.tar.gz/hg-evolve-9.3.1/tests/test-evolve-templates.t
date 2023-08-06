This test file test the various templates for predecessors and successors.

Global setup
============

  $ . $TESTDIR/testlib/common.sh
  $ cat >> $HGRCPATH <<EOF
  > [ui]
  > interactive = true
  > [phases]
  > publish=False
  > [experimental]
  > evolution.allowdivergence = True
  > [extensions]
  > evolve =
  > [alias]
  > tlog = log -G -T '{node|short}\
  >     {if(predecessors, "\n  Predecessors: {predecessors}")}\
  >     {if(predecessors, "\n  semi-colon: {join(predecessors, "; ")}")}\
  >     {if(successors, "\n  Successors: {successors}")}\
  >     {if(successors, "\n  semi-colon: {join(successors, "; ")}")}\
  >     {if(obsfate, "\n  Fate: {join(obsfate, "\n  Fate: ")}\n")}\n'
  > fatelog = log -G -T '{node|short}\n{if(obsfate, "  Obsfate: {join(obsfate, "; ")}\n\n")}'
  > EOF

Test templates on amended commit
================================

Test setup
----------

  $ hg init $TESTTMP/templates-local-amend
  $ cd $TESTTMP/templates-local-amend
  $ mkcommit ROOT
  $ mkcommit A0
  $ echo 42 >> A0
  $ HGUSER=test hg amend -m "A1" --config devel.default-date="1234567890 0"
  $ HGUSER=test2 hg amend -m "A2" --config devel.default-date="987654321 0"
  $ hg log --hidden -G
  @  changeset:   3:d004c8f274b9
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A2
  |
  | x  changeset:   2:a468dc9b3633
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 3:d004c8f274b9 by test2
  |    summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 2:a468dc9b3633
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check templates
---------------
  $ hg up 'desc(A0)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: d004c8f274b9)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: d004c8f274b9)

Predecessors template should show current revision as it is the working copy
  $ hg olog tip
  o  d004c8f274b9 (3) A2
  |
  x  a468dc9b3633 (2) A1
  |    reworded(description) as d004c8f274b9 using amend by test2 (Thu Apr 19 04:25:21 2001 +0000)
  |
  @  471f378eab4c (1) A0
       rewritten(description, content) as a468dc9b3633 using amend by test (Fri Feb 13 23:31:30 2009 +0000)
  
  $ hg tlog
  o  d004c8f274b9
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | @  471f378eab4c
  |/     Successors: 3:d004c8f274b9
  |      semi-colon: 3:d004c8f274b9
  |      Fate: rewritten using amend as 3:d004c8f274b9 by test, test2
  |
  o  ea207398892e
  

  $ hg log -G
  o  changeset:   3:d004c8f274b9
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A2
  |
  | @  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 3:d004c8f274b9 by test, test2
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  

  $ hg fatelog -q
  o  d004c8f274b9
  |
  | @  471f378eab4c
  |/     Obsfate: rewritten using amend as 3:d004c8f274b9
  |
  o  ea207398892e
  

  $ hg fatelog
  o  d004c8f274b9
  |
  | @  471f378eab4c
  |/     Obsfate: rewritten using amend as 3:d004c8f274b9 by test, test2
  |
  o  ea207398892e
  
  $ hg fatelog -v
  o  d004c8f274b9
  |
  | @  471f378eab4c
  |/     Obsfate: rewritten using amend as 3:d004c8f274b9 by test, test2 (between 2001-04-19 04:25 +0000 and 2009-02-13 23:31 +0000)
  |
  o  ea207398892e
  

(check json)

  $ hg log -GT '{predecessors|json}\n'
  o  ["471f378eab4c5e25f6c77f785b27c936efb22874"]
  |
  | @  []
  |/
  o  []
  

  $ hg log -GT '{successors|json}\n'
  o  ""
  |
  | @  [["d004c8f274b9ec480a47a93c10dac5eee63adb78"]]
  |/
  o  ""
  

  $ hg up 'desc(A1)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset a468dc9b3633
  (hidden revision 'a468dc9b3633' was rewritten as: d004c8f274b9)
  working directory parent is obsolete! (a468dc9b3633)
  (use 'hg evolve' to update to its successor: d004c8f274b9)

Predecessors template should show current revision as it is the working copy
  $ hg tlog
  o  d004c8f274b9
  |    Predecessors: 2:a468dc9b3633
  |    semi-colon: 2:a468dc9b3633
  | @  a468dc9b3633
  |/     Successors: 3:d004c8f274b9
  |      semi-colon: 3:d004c8f274b9
  |      Fate: reworded using amend as 3:d004c8f274b9 by test2
  |
  o  ea207398892e
  
Predecessors template should show the precursor as we force its display with
--hidden  
  $ hg tlog --hidden
  o  d004c8f274b9
  |    Predecessors: 2:a468dc9b3633
  |    semi-colon: 2:a468dc9b3633
  | @  a468dc9b3633
  |/     Predecessors: 1:471f378eab4c
  |      semi-colon: 1:471f378eab4c
  |      Successors: 3:d004c8f274b9
  |      semi-colon: 3:d004c8f274b9
  |      Fate: reworded using amend as 3:d004c8f274b9 by test2
  |
  | x  471f378eab4c
  |/     Successors: 2:a468dc9b3633
  |      semi-colon: 2:a468dc9b3633
  |      Fate: rewritten using amend as 2:a468dc9b3633
  |
  o  ea207398892e
  
  $ hg fatelog -v
  o  d004c8f274b9
  |
  | @  a468dc9b3633
  |/     Obsfate: reworded using amend as 3:d004c8f274b9 by test2 (at 2001-04-19 04:25 +0000)
  |
  o  ea207398892e
  
  $ hg up 'desc(A2)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg tlog
  @  d004c8f274b9
  |
  o  ea207398892e
  
  $ hg tlog --hidden
  @  d004c8f274b9
  |    Predecessors: 2:a468dc9b3633
  |    semi-colon: 2:a468dc9b3633
  | x  a468dc9b3633
  |/     Predecessors: 1:471f378eab4c
  |      semi-colon: 1:471f378eab4c
  |      Successors: 3:d004c8f274b9
  |      semi-colon: 3:d004c8f274b9
  |      Fate: reworded using amend as 3:d004c8f274b9 by test2
  |
  | x  471f378eab4c
  |/     Successors: 2:a468dc9b3633
  |      semi-colon: 2:a468dc9b3633
  |      Fate: rewritten using amend as 2:a468dc9b3633
  |
  o  ea207398892e
  
  $ hg fatelog -v
  @  d004c8f274b9
  |
  o  ea207398892e
  

  $ hg fatelog -v --hidden
  @  d004c8f274b9
  |
  | x  a468dc9b3633
  |/     Obsfate: reworded using amend as 3:d004c8f274b9 by test2 (at 2001-04-19 04:25 +0000)
  |
  | x  471f378eab4c
  |/     Obsfate: rewritten using amend as 2:a468dc9b3633 by test (at 2009-02-13 23:31 +0000)
  |
  o  ea207398892e
  

Test templates with split commit
================================

  $ hg init $TESTTMP/templates-local-split
  $ cd $TESTTMP/templates-local-split
  $ mkcommit ROOT
  $ echo 42 >> a
  $ echo 43 >> b
  $ hg commit -A -m "A0"
  adding a
  adding b
  $ hg log --hidden -G
  @  changeset:   1:471597cad322
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg split -r 'desc(A0)' -d "0 0" << EOF
  > y
  > y
  > n
  > y
  > y
  > y
  > EOF
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  adding a
  adding b
  diff --git a/a b/a
  new file mode 100644
  examine changes to 'a'?
  (enter ? for help) [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +42
  record change 1/2 to 'a'?
  (enter ? for help) [Ynesfdaq?] y
  
  diff --git a/b b/b
  new file mode 100644
  examine changes to 'b'?
  (enter ? for help) [Ynesfdaq?] n
  
  created new head
  continue splitting? [Ycdq?] y
  diff --git a/b b/b
  new file mode 100644
  examine changes to 'b'?
  (enter ? for help) [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +43
  record this change to 'b'?
  (enter ? for help) [Ynesfdaq?] y
  
  no more change to split

  $ hg log --hidden -G
  @  changeset:   3:f257fde29c7a
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   2:337fec4d2edc
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  | x  changeset:   1:471597cad322
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    split using split as 2:337fec4d2edc, 3:f257fde29c7a
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  

Check templates
---------------

  $ hg up 'obsolete()' --hidden
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471597cad322
  (hidden revision '471597cad322' was split as: 337fec4d2edc, f257fde29c7a)
  working directory parent is obsolete! (471597cad322)
  (use 'hg evolve' to update to its tipmost successor: 337fec4d2edc, f257fde29c7a)

Predecessors template should show current revision as it is the working copy
  $ hg tlog
  o  f257fde29c7a
  |    Predecessors: 1:471597cad322
  |    semi-colon: 1:471597cad322
  o  337fec4d2edc
  |    Predecessors: 1:471597cad322
  |    semi-colon: 1:471597cad322
  | @  471597cad322
  |/     Successors: 2:337fec4d2edc 3:f257fde29c7a
  |      semi-colon: 2:337fec4d2edc 3:f257fde29c7a
  |      Fate: split using split as 2:337fec4d2edc, 3:f257fde29c7a
  |
  o  ea207398892e
  
  $ hg fatelog
  o  f257fde29c7a
  |
  o  337fec4d2edc
  |
  | @  471597cad322
  |/     Obsfate: split using split as 2:337fec4d2edc, 3:f257fde29c7a
  |
  o  ea207398892e
  

  $ hg up f257fde29c7a
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

Predecessors template should not show a precursor as it's not displayed in the
log
  $ hg tlog
  @  f257fde29c7a
  |
  o  337fec4d2edc
  |
  o  ea207398892e
  
Predecessors template should show the precursor as we force its display with
--hidden
  $ hg tlog --hidden
  @  f257fde29c7a
  |    Predecessors: 1:471597cad322
  |    semi-colon: 1:471597cad322
  o  337fec4d2edc
  |    Predecessors: 1:471597cad322
  |    semi-colon: 1:471597cad322
  | x  471597cad322
  |/     Successors: 2:337fec4d2edc 3:f257fde29c7a
  |      semi-colon: 2:337fec4d2edc 3:f257fde29c7a
  |      Fate: split using split as 2:337fec4d2edc, 3:f257fde29c7a
  |
  o  ea207398892e
  
  $ hg fatelog --hidden
  @  f257fde29c7a
  |
  o  337fec4d2edc
  |
  | x  471597cad322
  |/     Obsfate: split using split as 2:337fec4d2edc, 3:f257fde29c7a
  |
  o  ea207398892e
  

Test templates with folded commit
==============================

Test setup
----------

  $ hg init $TESTTMP/templates-local-fold
  $ cd $TESTTMP/templates-local-fold
  $ mkcommit ROOT
  $ mkcommit A0
  $ mkcommit B0
  $ hg log --hidden -G
  @  changeset:   2:0dec01379d3b
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     B0
  |
  o  changeset:   1:471f378eab4c
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg fold --exact -r 'desc(A0) + desc(B0)' --date "0 0" -m "C0"
  2 changesets folded
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg log --hidden -G
  @  changeset:   3:eb5a0daa2192
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  | x  changeset:   2:0dec01379d3b
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  obsolete:    folded using fold as 3:eb5a0daa2192
  | |  summary:     B0
  | |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    folded using fold as 3:eb5a0daa2192
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check templates
---------------

  $ hg up 'desc(A0)' --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)

Predecessors template should show current revision as it is the working copy
  $ hg tlog
  o  eb5a0daa2192
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | @  471f378eab4c
  |/     Successors: 3:eb5a0daa2192
  |      semi-colon: 3:eb5a0daa2192
  |      Fate: folded using fold as 3:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog
  o  eb5a0daa2192
  |
  | @  471f378eab4c
  |/     Obsfate: folded using fold as 3:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg up 'desc(B0)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 0dec01379d3b
  (hidden revision '0dec01379d3b' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (0dec01379d3b)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)

Predecessors template should show both predecessors as they should be both
displayed
  $ hg tlog
  o  eb5a0daa2192
  |    Predecessors: 2:0dec01379d3b 1:471f378eab4c
  |    semi-colon: 2:0dec01379d3b; 1:471f378eab4c
  | @  0dec01379d3b
  | |    Successors: 3:eb5a0daa2192
  | |    semi-colon: 3:eb5a0daa2192
  | |    Fate: folded using fold as 3:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Successors: 3:eb5a0daa2192
  |      semi-colon: 3:eb5a0daa2192
  |      Fate: folded using fold as 3:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog
  o  eb5a0daa2192
  |
  | @  0dec01379d3b
  | |    Obsfate: folded using fold as 3:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Obsfate: folded using fold as 3:eb5a0daa2192
  |
  o  ea207398892e
  

  $ hg up 'desc(C0)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

Predecessors template should not show predecessors as it's not displayed in the
log
  $ hg tlog
  @  eb5a0daa2192
  |
  o  ea207398892e
  
Predecessors template should show both predecessors as we force its display with
--hidden
  $ hg tlog --hidden
  @  eb5a0daa2192
  |    Predecessors: 2:0dec01379d3b 1:471f378eab4c
  |    semi-colon: 2:0dec01379d3b; 1:471f378eab4c
  | x  0dec01379d3b
  | |    Successors: 3:eb5a0daa2192
  | |    semi-colon: 3:eb5a0daa2192
  | |    Fate: folded using fold as 3:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Successors: 3:eb5a0daa2192
  |      semi-colon: 3:eb5a0daa2192
  |      Fate: folded using fold as 3:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog --hidden
  @  eb5a0daa2192
  |
  | x  0dec01379d3b
  | |    Obsfate: folded using fold as 3:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Obsfate: folded using fold as 3:eb5a0daa2192
  |
  o  ea207398892e
  

Test templates with divergence
==============================

Test setup
----------

  $ hg init $TESTTMP/templates-local-divergence
  $ cd $TESTTMP/templates-local-divergence
  $ mkcommit ROOT
  $ mkcommit A0
  $ hg amend -m "A1"
  $ hg log --hidden -G
  @  changeset:   2:fdf9bde5129a
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 2:fdf9bde5129a
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg update --hidden 'desc(A0)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: fdf9bde5129a)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: fdf9bde5129a)
  $ hg amend -m "A2"
  2 new content-divergent changesets
  $ hg log --hidden -G
  @  changeset:   3:65b757b745b9
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     A2
  |
  | *  changeset:   2:fdf9bde5129a
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 2:fdf9bde5129a
  |    obsolete:    reworded using amend as 3:65b757b745b9
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg amend -m 'A3'

Check templates
---------------

  $ hg up 'desc(A0)' --hidden
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' has diverged)
  working directory parent is obsolete! (471f378eab4c)
  (471f378eab4c has diverged, use 'hg evolve --list --content-divergent' to resolve the issue)

Predecessors template should show current revision as it is the working copy
  $ hg tlog
  *  019fadeab383
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | *  fdf9bde5129a
  |/     Predecessors: 1:471f378eab4c
  |      semi-colon: 1:471f378eab4c
  | @  471f378eab4c
  |/     Successors: 2:fdf9bde5129a; 4:019fadeab383
  |      semi-colon: 2:fdf9bde5129a; 4:019fadeab383
  |      Fate: reworded using amend as 2:fdf9bde5129a
  |      Fate: reworded using amend as 4:019fadeab383
  |
  o  ea207398892e
  
  $ hg fatelog
  *  019fadeab383
  |
  | *  fdf9bde5129a
  |/
  | @  471f378eab4c
  |/     Obsfate: reworded using amend as 2:fdf9bde5129a; reworded using amend as 4:019fadeab383
  |
  o  ea207398892e
  

  $ hg up 'desc(A1)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
Predecessors template should not show predecessors as it's not displayed in the
log
  $ hg tlog
  *  019fadeab383
  |
  | @  fdf9bde5129a
  |/
  o  ea207398892e
  

  $ hg fatelog
  *  019fadeab383
  |
  | @  fdf9bde5129a
  |/
  o  ea207398892e
  
Predecessors template should a precursor as we force its display with --hidden
  $ hg tlog --hidden
  *  019fadeab383
  |    Predecessors: 3:65b757b745b9
  |    semi-colon: 3:65b757b745b9
  | x  65b757b745b9
  |/     Predecessors: 1:471f378eab4c
  |      semi-colon: 1:471f378eab4c
  |      Successors: 4:019fadeab383
  |      semi-colon: 4:019fadeab383
  |      Fate: reworded using amend as 4:019fadeab383
  |
  | @  fdf9bde5129a
  |/     Predecessors: 1:471f378eab4c
  |      semi-colon: 1:471f378eab4c
  | x  471f378eab4c
  |/     Successors: 2:fdf9bde5129a; 3:65b757b745b9
  |      semi-colon: 2:fdf9bde5129a; 3:65b757b745b9
  |      Fate: reworded using amend as 2:fdf9bde5129a
  |      Fate: reworded using amend as 3:65b757b745b9
  |
  o  ea207398892e
  
  $ hg fatelog --hidden
  *  019fadeab383
  |
  | x  65b757b745b9
  |/     Obsfate: reworded using amend as 4:019fadeab383
  |
  | @  fdf9bde5129a
  |/
  | x  471f378eab4c
  |/     Obsfate: reworded using amend as 2:fdf9bde5129a; reworded using amend as 3:65b757b745b9
  |
  o  ea207398892e
  

Test templates with amended + folded commit
===========================================

Test setup
----------

  $ hg init $TESTTMP/templates-local-amend-fold
  $ cd $TESTTMP/templates-local-amend-fold
  $ mkcommit ROOT
  $ mkcommit A0
  $ mkcommit B0
  $ hg amend -m "B1"
  $ hg log --hidden -G
  @  changeset:   3:b7ea6d14e664
  |  tag:         tip
  |  parent:      1:471f378eab4c
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     B1
  |
  | x  changeset:   2:0dec01379d3b
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 3:b7ea6d14e664
  |    summary:     B0
  |
  o  changeset:   1:471f378eab4c
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg fold --exact -r 'desc(A0) + desc(B1)' --date "0 0" -m "C0"
  2 changesets folded
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg log --hidden -G
  @  changeset:   4:eb5a0daa2192
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  | x  changeset:   3:b7ea6d14e664
  | |  parent:      1:471f378eab4c
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  obsolete:    folded using fold as 4:eb5a0daa2192
  | |  summary:     B1
  | |
  | | x  changeset:   2:0dec01379d3b
  | |/   user:        test
  | |    date:        Thu Jan 01 00:00:00 1970 +0000
  | |    obsolete:    reworded using amend as 3:b7ea6d14e664
  | |    summary:     B0
  | |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    folded using fold as 4:eb5a0daa2192
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check templates
---------------

  $ hg up 'desc(A0)' --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)
  $ hg tlog
  o  eb5a0daa2192
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | @  471f378eab4c
  |/     Successors: 4:eb5a0daa2192
  |      semi-colon: 4:eb5a0daa2192
  |      Fate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog
  o  eb5a0daa2192
  |
  | @  471f378eab4c
  |/     Obsfate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg up 'desc(B0)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 0dec01379d3b
  (hidden revision '0dec01379d3b' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (0dec01379d3b)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)
  $ hg tlog
  o  eb5a0daa2192
  |    Predecessors: 2:0dec01379d3b 1:471f378eab4c
  |    semi-colon: 2:0dec01379d3b; 1:471f378eab4c
  | @  0dec01379d3b
  | |    Successors: 4:eb5a0daa2192
  | |    semi-colon: 4:eb5a0daa2192
  | |    Fate: rewritten using amend, fold as 4:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Successors: 4:eb5a0daa2192
  |      semi-colon: 4:eb5a0daa2192
  |      Fate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog
  o  eb5a0daa2192
  |
  | @  0dec01379d3b
  | |    Obsfate: rewritten using amend, fold as 4:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Obsfate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  

  $ hg up 'desc(B1)' --hidden
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset b7ea6d14e664
  (hidden revision 'b7ea6d14e664' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (b7ea6d14e664)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)
  $ hg tlog
  o  eb5a0daa2192
  |    Predecessors: 1:471f378eab4c 3:b7ea6d14e664
  |    semi-colon: 1:471f378eab4c; 3:b7ea6d14e664
  | @  b7ea6d14e664
  | |    Successors: 4:eb5a0daa2192
  | |    semi-colon: 4:eb5a0daa2192
  | |    Fate: folded using fold as 4:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Successors: 4:eb5a0daa2192
  |      semi-colon: 4:eb5a0daa2192
  |      Fate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog
  o  eb5a0daa2192
  |
  | @  b7ea6d14e664
  | |    Obsfate: folded using fold as 4:eb5a0daa2192
  | |
  | x  471f378eab4c
  |/     Obsfate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  

  $ hg up 'desc(C0)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg tlog
  @  eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg tlog --hidden
  @  eb5a0daa2192
  |    Predecessors: 1:471f378eab4c 3:b7ea6d14e664
  |    semi-colon: 1:471f378eab4c; 3:b7ea6d14e664
  | x  b7ea6d14e664
  | |    Predecessors: 2:0dec01379d3b
  | |    semi-colon: 2:0dec01379d3b
  | |    Successors: 4:eb5a0daa2192
  | |    semi-colon: 4:eb5a0daa2192
  | |    Fate: folded using fold as 4:eb5a0daa2192
  | |
  | | x  0dec01379d3b
  | |/     Successors: 3:b7ea6d14e664
  | |      semi-colon: 3:b7ea6d14e664
  | |      Fate: reworded using amend as 3:b7ea6d14e664
  | |
  | x  471f378eab4c
  |/     Successors: 4:eb5a0daa2192
  |      semi-colon: 4:eb5a0daa2192
  |      Fate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  
  $ hg fatelog --hidden
  @  eb5a0daa2192
  |
  | x  b7ea6d14e664
  | |    Obsfate: folded using fold as 4:eb5a0daa2192
  | |
  | | x  0dec01379d3b
  | |/     Obsfate: reworded using amend as 3:b7ea6d14e664
  | |
  | x  471f378eab4c
  |/     Obsfate: folded using fold as 4:eb5a0daa2192
  |
  o  ea207398892e
  

Test template with pushed and pulled obs markers
==============================================

Test setup
----------

  $ hg init $TESTTMP/templates-local-remote-markers-1
  $ cd $TESTTMP/templates-local-remote-markers-1
  $ mkcommit ROOT
  $ mkcommit A0  
  $ hg clone $TESTTMP/templates-local-remote-markers-1 $TESTTMP/templates-local-remote-markers-2
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd $TESTTMP/templates-local-remote-markers-2
  $ hg log --hidden -G
  @  changeset:   1:471f378eab4c
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ cd $TESTTMP/templates-local-remote-markers-1
  $ hg amend -m "A1"
  $ hg amend -m "A2"
  $ hg log --hidden -G
  @  changeset:   3:7a230b46bf61
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A2
  |
  | x  changeset:   2:fdf9bde5129a
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 3:7a230b46bf61
  |    summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 2:fdf9bde5129a
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ cd $TESTTMP/templates-local-remote-markers-2
  $ hg pull
  pulling from $TESTTMP/templates-local-remote-markers-1
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 0 changes to 1 files (+1 heads)
  2 new obsolescence markers
  obsoleted 1 changesets
  new changesets 7a230b46bf61 (1 drafts)
  (run 'hg heads' to see heads, 'hg merge' to merge)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: 7a230b46bf61)
  $ hg log --hidden -G
  o  changeset:   2:7a230b46bf61
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A2
  |
  | @  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 2:7a230b46bf61
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check templates
---------------

  $ hg tlog
  o  7a230b46bf61
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | @  471f378eab4c
  |/     Successors: 2:7a230b46bf61
  |      semi-colon: 2:7a230b46bf61
  |      Fate: reworded using amend as 2:7a230b46bf61
  |
  o  ea207398892e
  
  $ hg fatelog --hidden -v
  o  7a230b46bf61
  |
  | @  471f378eab4c
  |/     Obsfate: reworded using amend as 2:7a230b46bf61 by test (at 1970-01-01 00:00 +0000)
  |
  o  ea207398892e
  
  $ hg up 'desc(A2)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg tlog
  @  7a230b46bf61
  |
  o  ea207398892e
  
  $ hg fatelog -v
  @  7a230b46bf61
  |
  o  ea207398892e
  
  $ hg tlog --hidden
  @  7a230b46bf61
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | x  471f378eab4c
  |/     Successors: 2:7a230b46bf61
  |      semi-colon: 2:7a230b46bf61
  |      Fate: reworded using amend as 2:7a230b46bf61
  |
  o  ea207398892e
  
  $ hg fatelog --hidden -v
  @  7a230b46bf61
  |
  | x  471f378eab4c
  |/     Obsfate: reworded using amend as 2:7a230b46bf61 by test (at 1970-01-01 00:00 +0000)
  |
  o  ea207398892e
  
 
Test template with obsmarkers cycle
===================================

Test setup
----------

  $ hg init $TESTTMP/templates-local-cycle
  $ cd $TESTTMP/templates-local-cycle
  $ mkcommit ROOT
  $ mkcommit A0
  $ mkcommit B0
  $ hg up -r 0
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ mkcommit C0
  created new head

Create the cycle

  $ hg debugobsolete `getid "desc(A0)"` `getid "desc(B0)"`
  1 new obsolescence markers
  obsoleted 1 changesets
  1 new orphan changesets
  $ hg debugobsolete `getid "desc(B0)"` `getid "desc(C0)"`
  1 new obsolescence markers
  obsoleted 1 changesets
  $ hg debugobsolete `getid "desc(B0)"` `getid "desc(A0)"`
  1 new obsolescence markers

Check templates
---------------

  $ hg tlog
  @  f897c6137566
  |
  o  ea207398892e
  
  $ hg fatelog
  @  f897c6137566
  |
  o  ea207398892e
  
  $ hg up -r "desc(B0)" --hidden
  2 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset 0dec01379d3b
  (hidden revision '0dec01379d3b' is pruned)
  working directory parent is obsolete! (0dec01379d3b)
  (use 'hg evolve' to update to its parent successor)
  $ hg tlog
  o  f897c6137566
  |    Predecessors: 2:0dec01379d3b
  |    semi-colon: 2:0dec01379d3b
  | @  0dec01379d3b
  | |    Predecessors: 1:471f378eab4c
  | |    semi-colon: 1:471f378eab4c
  | |    Successors: 3:f897c6137566; 1:471f378eab4c
  | |    semi-colon: 3:f897c6137566; 1:471f378eab4c
  | |    Fate: rewritten as 3:f897c6137566
  | |    Fate: rewritten as 1:471f378eab4c
  | |
  | x  471f378eab4c
  |/     Predecessors: 2:0dec01379d3b
  |      semi-colon: 2:0dec01379d3b
  |      Successors: 2:0dec01379d3b
  |      semi-colon: 2:0dec01379d3b
  |      Fate: rewritten as 2:0dec01379d3b
  |
  o  ea207398892e
  
  $ hg fatelog
  o  f897c6137566
  |
  | @  0dec01379d3b
  | |    Obsfate: rewritten as 3:f897c6137566; rewritten as 1:471f378eab4c
  | |
  | x  471f378eab4c
  |/     Obsfate: rewritten as 2:0dec01379d3b
  |
  o  ea207398892e
  
  $ hg up -r "desc(A0)" --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its parent successor)
  $ hg tlog
  o  f897c6137566
  |    Predecessors: 1:471f378eab4c
  |    semi-colon: 1:471f378eab4c
  | @  471f378eab4c
  |/     Fate: pruned
  |
  o  ea207398892e
  
  $ hg fatelog
  o  f897c6137566
  |
  | @  471f378eab4c
  |/     Obsfate: pruned
  |
  o  ea207398892e
  

  $ hg up -r "desc(ROOT)" --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg tlog
  o  f897c6137566
  |
  @  ea207398892e
  
  $ hg fatelog
  o  f897c6137566
  |
  @  ea207398892e
  
  $ hg tlog --hidden
  o  f897c6137566
  |    Predecessors: 2:0dec01379d3b
  |    semi-colon: 2:0dec01379d3b
  | x  0dec01379d3b
  | |    Predecessors: 1:471f378eab4c
  | |    semi-colon: 1:471f378eab4c
  | |    Successors: 3:f897c6137566; 1:471f378eab4c
  | |    semi-colon: 3:f897c6137566; 1:471f378eab4c
  | |    Fate: rewritten as 3:f897c6137566
  | |    Fate: rewritten as 1:471f378eab4c
  | |
  | x  471f378eab4c
  |/     Predecessors: 2:0dec01379d3b
  |      semi-colon: 2:0dec01379d3b
  |      Successors: 2:0dec01379d3b
  |      semi-colon: 2:0dec01379d3b
  |      Fate: rewritten as 2:0dec01379d3b
  |
  @  ea207398892e
  
Test template with split + divergence with cycles
=================================================

  $ hg log -G
  o  changeset:   3:f897c6137566
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  @  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg up
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved

Create a commit with three files
  $ touch A B C
  $ hg commit -A -m "Add A,B,C" A B C

Split it
  $ hg up 3
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ touch A
  $ hg commit -A -m "Add A,B,C" A
  created new head

  $ touch B
  $ hg commit -A -m "Add A,B,C" B

  $ touch C
  $ hg commit -A -m "Add A,B,C" C

  $ hg log -G
  @  changeset:   7:ba2ed02b0c9a
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     Add A,B,C
  |
  o  changeset:   6:4a004186e638
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     Add A,B,C
  |
  o  changeset:   5:dd800401bd8c
  |  parent:      3:f897c6137566
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     Add A,B,C
  |
  | o  changeset:   4:9bd10a0775e4
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     Add A,B,C
  |
  o  changeset:   3:f897c6137566
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg debugobsolete `getid "4"` `getid "5"` `getid "6"` `getid "7"`
  1 new obsolescence markers
  obsoleted 1 changesets
  $ hg log -G
  @  changeset:   7:ba2ed02b0c9a
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     Add A,B,C
  |
  o  changeset:   6:4a004186e638
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     Add A,B,C
  |
  o  changeset:   5:dd800401bd8c
  |  parent:      3:f897c6137566
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     Add A,B,C
  |
  o  changeset:   3:f897c6137566
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Diverge one of the split commit

  $ hg up 6
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg commit --amend -m "Add only B"
  1 new orphan changesets

  $ hg up 6 --hidden
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory parent is obsolete! (4a004186e638)
  (use 'hg evolve' to update to its successor: b18bc8331526)
  $ hg commit --amend -m "Add B only"
  4 new content-divergent changesets

  $ hg log -G
  @  changeset:   9:0b997eb7ceee
  |  tag:         tip
  |  parent:      5:dd800401bd8c
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     Add B only
  |
  | *  changeset:   8:b18bc8331526
  |/   parent:      5:dd800401bd8c
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     Add only B
  |
  | *  changeset:   7:ba2ed02b0c9a
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  instability: orphan, content-divergent
  | |  summary:     Add A,B,C
  | |
  | x  changeset:   6:4a004186e638
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 8:b18bc8331526
  |    obsolete:    reworded using amend as 9:0b997eb7ceee
  |    summary:     Add A,B,C
  |
  *  changeset:   5:dd800401bd8c
  |  parent:      3:f897c6137566
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     Add A,B,C
  |
  o  changeset:   3:f897c6137566
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check templates
---------------

  $ hg tlog
  @  0b997eb7ceee
  |    Predecessors: 6:4a004186e638
  |    semi-colon: 6:4a004186e638
  | *  b18bc8331526
  |/     Predecessors: 6:4a004186e638
  |      semi-colon: 6:4a004186e638
  | *  ba2ed02b0c9a
  | |
  | x  4a004186e638
  |/     Successors: 8:b18bc8331526; 9:0b997eb7ceee
  |      semi-colon: 8:b18bc8331526; 9:0b997eb7ceee
  |      Fate: reworded using amend as 8:b18bc8331526
  |      Fate: reworded using amend as 9:0b997eb7ceee
  |
  *  dd800401bd8c
  |
  o  f897c6137566
  |
  o  ea207398892e
  
  $ hg fatelog
  @  0b997eb7ceee
  |
  | *  b18bc8331526
  |/
  | *  ba2ed02b0c9a
  | |
  | x  4a004186e638
  |/     Obsfate: reworded using amend as 8:b18bc8331526; reworded using amend as 9:0b997eb7ceee
  |
  *  dd800401bd8c
  |
  o  f897c6137566
  |
  o  ea207398892e
  
  $ hg tlog --hidden
  @  0b997eb7ceee
  |    Predecessors: 6:4a004186e638
  |    semi-colon: 6:4a004186e638
  | *  b18bc8331526
  |/     Predecessors: 6:4a004186e638
  |      semi-colon: 6:4a004186e638
  | *  ba2ed02b0c9a
  | |    Predecessors: 4:9bd10a0775e4
  | |    semi-colon: 4:9bd10a0775e4
  | x  4a004186e638
  |/     Predecessors: 4:9bd10a0775e4
  |      semi-colon: 4:9bd10a0775e4
  |      Successors: 8:b18bc8331526; 9:0b997eb7ceee
  |      semi-colon: 8:b18bc8331526; 9:0b997eb7ceee
  |      Fate: reworded using amend as 8:b18bc8331526
  |      Fate: reworded using amend as 9:0b997eb7ceee
  |
  *  dd800401bd8c
  |    Predecessors: 4:9bd10a0775e4
  |    semi-colon: 4:9bd10a0775e4
  | x  9bd10a0775e4
  |/     Successors: 5:dd800401bd8c 6:4a004186e638 7:ba2ed02b0c9a
  |      semi-colon: 5:dd800401bd8c 6:4a004186e638 7:ba2ed02b0c9a
  |      Fate: split as 5:dd800401bd8c, 6:4a004186e638, 7:ba2ed02b0c9a
  |
  o  f897c6137566
  |    Predecessors: 2:0dec01379d3b
  |    semi-colon: 2:0dec01379d3b
  | x  0dec01379d3b
  | |    Predecessors: 1:471f378eab4c
  | |    semi-colon: 1:471f378eab4c
  | |    Successors: 3:f897c6137566; 1:471f378eab4c
  | |    semi-colon: 3:f897c6137566; 1:471f378eab4c
  | |    Fate: rewritten as 3:f897c6137566
  | |    Fate: rewritten as 1:471f378eab4c
  | |
  | x  471f378eab4c
  |/     Predecessors: 2:0dec01379d3b
  |      semi-colon: 2:0dec01379d3b
  |      Successors: 2:0dec01379d3b
  |      semi-colon: 2:0dec01379d3b
  |      Fate: rewritten as 2:0dec01379d3b
  |
  o  ea207398892e
  
  $ hg fatelog --hidden
  @  0b997eb7ceee
  |
  | *  b18bc8331526
  |/
  | *  ba2ed02b0c9a
  | |
  | x  4a004186e638
  |/     Obsfate: reworded using amend as 8:b18bc8331526; reworded using amend as 9:0b997eb7ceee
  |
  *  dd800401bd8c
  |
  | x  9bd10a0775e4
  |/     Obsfate: split as 5:dd800401bd8c, 6:4a004186e638, 7:ba2ed02b0c9a
  |
  o  f897c6137566
  |
  | x  0dec01379d3b
  | |    Obsfate: rewritten as 3:f897c6137566; rewritten as 1:471f378eab4c
  | |
  | x  471f378eab4c
  |/     Obsfate: rewritten as 2:0dec01379d3b
  |
  o  ea207398892e
  
  $ hg up --hidden 4
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 9bd10a0775e4
  (hidden revision '9bd10a0775e4' has diverged)
  working directory parent is obsolete! (9bd10a0775e4)
  (9bd10a0775e4 has diverged, use 'hg evolve --list --content-divergent' to resolve the issue)
  $ hg rebase -r 7 -d 8 --config extensions.rebase=
  rebasing 7:ba2ed02b0c9a "Add A,B,C"
  $ hg tlog
  *  eceed8f98ffc
  |    Predecessors: 4:9bd10a0775e4
  |    semi-colon: 4:9bd10a0775e4
  | *  0b997eb7ceee
  | |    Predecessors: 4:9bd10a0775e4
  | |    semi-colon: 4:9bd10a0775e4
  * |  b18bc8331526
  |/     Predecessors: 4:9bd10a0775e4
  |      semi-colon: 4:9bd10a0775e4
  *  dd800401bd8c
  |    Predecessors: 4:9bd10a0775e4
  |    semi-colon: 4:9bd10a0775e4
  | @  9bd10a0775e4
  |/     Successors: 5:dd800401bd8c 9:0b997eb7ceee 10:eceed8f98ffc; 5:dd800401bd8c 8:b18bc8331526 10:eceed8f98ffc
  |      semi-colon: 5:dd800401bd8c 9:0b997eb7ceee 10:eceed8f98ffc; 5:dd800401bd8c 8:b18bc8331526 10:eceed8f98ffc
  |      Fate: split using amend, rebase as 5:dd800401bd8c, 9:0b997eb7ceee, 10:eceed8f98ffc
  |      Fate: split using amend, rebase as 5:dd800401bd8c, 8:b18bc8331526, 10:eceed8f98ffc
  |
  o  f897c6137566
  |
  o  ea207398892e
  
  $ hg fatelog
  *  eceed8f98ffc
  |
  | *  0b997eb7ceee
  | |
  * |  b18bc8331526
  |/
  *  dd800401bd8c
  |
  | @  9bd10a0775e4
  |/     Obsfate: split using amend, rebase as 5:dd800401bd8c, 9:0b997eb7ceee, 10:eceed8f98ffc; split using amend, rebase as 5:dd800401bd8c, 8:b18bc8331526, 10:eceed8f98ffc
  |
  o  f897c6137566
  |
  o  ea207398892e
  
Test templates with pruned commits
==================================

Test setup
----------

  $ hg init $TESTTMP/templates-local-prune
  $ cd $TESTTMP/templates-local-prune
  $ mkcommit ROOT
  $ mkcommit A0
  $ hg prune .
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory is now at ea207398892e
  1 changesets pruned

Check output
------------

  $ hg up "desc(A0)" --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' is pruned)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its parent successor)
  $ hg tlog
  @  471f378eab4c
  |    Fate: pruned using prune
  |
  o  ea207398892e
  
  $ hg fatelog -v
  @  471f378eab4c
  |    Obsfate: pruned using prune by test (at 1970-01-01 00:00 +0000)
  |
  o  ea207398892e
  
