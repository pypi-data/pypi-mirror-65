This test file test the rewind command in several situations.

Global setup
============

  $ . $TESTDIR/testlib/common.sh
  $ cat >> $HGRCPATH <<EOF
  > [ui]
  > interactive = true
  > [phases]
  > publish=False
  > [alias]
  > glf = log -GT "{rev}: {desc} ({files})"
  > [extensions]
  > evolve =
  > EOF

  $ hg init rewind-testing-base
  $ cd rewind-testing-base
  $ echo a > root
  $ hg add root
  $ hg ci -m 'c_ROOT'
  $ echo a > A
  $ hg add A
  $ hg ci -m 'c_A0'
  $ echo a > B
  $ hg add B
  $ hg ci -m 'c_B0'
  $ hg log -G
  @  changeset:   2:7e594302a05d
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

  $ cd ..

Test rewinding to single changesets
====================================

  $ hg clone rewind-testing-base rewind-testing-simple-prune
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-simple-prune

Prune changeset unrelated to the working copy
---------------------------------------------

Setup
`````

Update to an unrelated changeset

  $ hg up 'desc("c_ROOT")'
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved

Prune the head

  $ hg prune -r 'desc("c_B0")'
  1 changesets pruned
  $ hg log -G
  o  changeset:   1:579f120ba918
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'desc("c_B0")'
  rewinded to 1 changesets
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 073989a581cf430a844192364fa37606357cbbc2 4 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog -r 'desc("c_B0")'
  o  073989a581cf (3) c_B0
  |
  x  7e594302a05d (2) c_B0
       pruned using prune by test (Thu Jan 01 00:00:00 1970 +0000)
       meta-changed(meta) as 073989a581cf using rewind by test (Thu Jan 01 00:00:00 1970 +0000)
  
  $ hg log -G
  o  changeset:   3:073989a581cf
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
XXX-TODO: fix the obsfate from "meta-changed as 3" to "identical" or something.

  $ hg log -G --hidden
  o  changeset:   3:073989a581cf
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    meta-changed using rewind as 3:073989a581cf
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Other independant rewind create a different revision
----------------------------------------------------------

setup
`````

note: we use "default-date" to make it a "different rewind"

  $ echo '[devel]' >> $HGRCPATH
  $ echo 'default-date = 1 0' >> $HGRCPATH

Actual rewind
`````````````

  $ hg prune 'desc("c_B0")'
  1 changesets pruned
  $ hg rewind --hidden --to 'min(desc("c_B0"))'
  rewinded to 1 changesets
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 073989a581cf430a844192364fa37606357cbbc2 4 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  073989a581cf430a844192364fa37606357cbbc2 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 b13b032065ef57a68d9a4cead38ba0f34f95529b 4 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog -r 'desc("c_B0")' --all
  x  073989a581cf (3) c_B0
  |    pruned using prune by test (Thu Jan 01 00:00:01 1970 +0000)
  |
  | o  b13b032065ef (4) c_B0
  |/
  x  7e594302a05d (2) c_B0
       pruned using prune by test (Thu Jan 01 00:00:00 1970 +0000)
       meta-changed(meta) as 073989a581cf using rewind by test (Thu Jan 01 00:00:00 1970 +0000)
       meta-changed(meta) as b13b032065ef using rewind by test (Thu Jan 01 00:00:01 1970 +0000)
  
  $ hg log -G
  o  changeset:   4:b13b032065ef
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg log -G --hidden
  o  changeset:   4:b13b032065ef
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  | x  changeset:   3:073989a581cf
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    pruned using prune
  |    summary:     c_B0
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    meta-changed using rewind as 4:b13b032065ef
  |    obsolete:    meta-changed using rewind as 3:073989a581cf
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

rewind a simple amend - creating content-divergence
---------------------------------------------------

Setup
`````

  $ hg clone rewind-testing-base rewind-testing-single-rewrite
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-single-rewrite
  $ echo BB > B
  $ hg amend -m 'c_B1'
  $ hg log -G
  @  changeset:   3:25c8f5ab0c3b
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B1
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'desc("c_B0")' --as-divergence
  2 new content-divergent changesets
  rewinded to 1 changesets
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 25c8f5ab0c3bb569ec672570f1a901be4c6f032b 0 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 b13b032065ef57a68d9a4cead38ba0f34f95529b 4 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog --rev 'desc("c_B0")'
  *  b13b032065ef (4) c_B0
  |
  x  7e594302a05d (2) c_B0
       rewritten(description, content) as 25c8f5ab0c3b using amend by test (Thu Jan 01 00:00:01 1970 +0000)
       meta-changed(meta) as b13b032065ef using rewind by test (Thu Jan 01 00:00:01 1970 +0000)
  
  $ hg log -G
  *  changeset:   4:b13b032065ef
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     c_B0
  |
  | @  changeset:   3:25c8f5ab0c3b
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     c_B1
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg log -G --hidden
  *  changeset:   4:b13b032065ef
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     c_B0
  |
  | @  changeset:   3:25c8f5ab0c3b
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     c_B1
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    meta-changed using rewind as 4:b13b032065ef
  |    obsolete:    rewritten using amend as 3:25c8f5ab0c3b
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Cleanup
```````
  $ hg prune 'max(desc("c_B0"))'
  1 changesets pruned
  $ hg log -G
  @  changeset:   3:25c8f5ab0c3b
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B1
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ echo 'default-date = 2 0' >> $HGRCPATH

rewind a simple amend - obsoleting the current latest successors
----------------------------------------------------------------

  $ hg rewind --hidden --to 'min(desc("c_B0"))'
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at 837cd997bb05
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 25c8f5ab0c3bb569ec672570f1a901be4c6f032b 0 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 b13b032065ef57a68d9a4cead38ba0f34f95529b 4 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  b13b032065ef57a68d9a4cead38ba0f34f95529b 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 837cd997bb05a27f8ed7d1ba3ff1e8422b9b464e 4 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  25c8f5ab0c3bb569ec672570f1a901be4c6f032b 837cd997bb05a27f8ed7d1ba3ff1e8422b9b464e 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '11', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog --rev 'desc("c_B0")'
  @    837cd997bb05 (5) c_B0
  |\
  x |  25c8f5ab0c3b (3) c_B1
  |/     rewritten(description, meta, content) as 837cd997bb05 using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(description, content) as 25c8f5ab0c3b using amend by test (Thu Jan 01 00:00:01 1970 +0000)
       meta-changed(meta) as 837cd997bb05 using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
       meta-changed(meta) as b13b032065ef using rewind by test (Thu Jan 01 00:00:01 1970 +0000)
  
  $ hg log -G
  @  changeset:   5:837cd997bb05
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg log -G --hidden
  @  changeset:   5:837cd997bb05
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  | x  changeset:   4:b13b032065ef
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    pruned using prune
  |    summary:     c_B0
  |
  | x  changeset:   3:25c8f5ab0c3b
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using rewind as 5:837cd997bb05
  |    summary:     c_B1
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    meta-changed using rewind as 4:b13b032065ef
  |    obsolete:    meta-changed using rewind as 5:837cd997bb05
  |    obsolete:    rewritten using amend as 3:25c8f5ab0c3b
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

rewind a simple split
---------------------

Setup
`````

  $ hg clone rewind-testing-base rewind-testing-split-fold
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-split-fold

  $ echo C > C
  $ echo D > D
  $ hg add C D
  $ hg ci -m 'c_CD0'
  $ hg split << EOF
  > y
  > f
  > d
  > c
  > EOF
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  adding C
  adding D
  diff --git a/C b/C
  new file mode 100644
  examine changes to 'C'?
  (enter ? for help) [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +C
  record change 1/2 to 'C'?
  (enter ? for help) [Ynesfdaq?] f
  
  diff --git a/D b/D
  new file mode 100644
  examine changes to 'D'?
  (enter ? for help) [Ynesfdaq?] d
  
  created new head
  continue splitting? [Ycdq?] c
  $ hg log -G
  @  changeset:   5:9576e80d6851
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   4:a0316c4c5417
  |  parent:      2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg debugobsolete
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e a0316c4c54179357e71d068fb8884678ebc7c351 9576e80d6851ce79cd535e2dc5fa01b444d89a39 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  $ hg obslog --all
  @  9576e80d6851 (5) c_CD0
  |
  | o  a0316c4c5417 (4) c_CD0
  |/
  x  49fb7d900906 (3) c_CD0
       split(parent, content) as 9576e80d6851, a0316c4c5417 using split by test (Thu Jan 01 00:00:02 1970 +0000)
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'min(desc("c_CD0"))'
  rewinded to 1 changesets
  (2 changesets obsoleted)
  working directory is now at 4535d0af405c
  $ hg debugobsolete
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e a0316c4c54179357e71d068fb8884678ebc7c351 9576e80d6851ce79cd535e2dc5fa01b444d89a39 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 4 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  9576e80d6851ce79cd535e2dc5fa01b444d89a39 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '14', 'operation': 'rewind', 'user': 'test'}
  a0316c4c54179357e71d068fb8884678ebc7c351 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '10', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    4535d0af405c (6) c_CD0
  |\
  | \
  | |\
  | x |  9576e80d6851 (5) c_CD0
  |/ /     rewritten(meta, parent, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  | |
  | x  a0316c4c5417 (4) c_CD0
  |/     rewritten(meta, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  |
  x  49fb7d900906 (3) c_CD0
       meta-changed(meta) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
       split(parent, content) as 9576e80d6851, a0316c4c5417 using split by test (Thu Jan 01 00:00:02 1970 +0000)
  
  $ hg log -G
  @  changeset:   6:4535d0af405c
  |  tag:         tip
  |  parent:      2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

rewind a fold
-------------

setup
`````

  $ echo 'default-date = 3 0' >> $HGRCPATH

Actual Rewind
`````````````

  $ hg rewind --to '9576e80d6851+a0316c4c5417' --hidden
  rewinded to 2 changesets
  (1 changesets obsoleted)
  working directory is now at 95d72d892df7
  $ hg debugobsolete
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e a0316c4c54179357e71d068fb8884678ebc7c351 9576e80d6851ce79cd535e2dc5fa01b444d89a39 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 4 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  9576e80d6851ce79cd535e2dc5fa01b444d89a39 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '14', 'operation': 'rewind', 'user': 'test'}
  a0316c4c54179357e71d068fb8884678ebc7c351 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '10', 'operation': 'rewind', 'user': 'test'}
  a0316c4c54179357e71d068fb8884678ebc7c351 e76375de0bfc9c59bdd91067c901f3eed7d6c8fe 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  9576e80d6851ce79cd535e2dc5fa01b444d89a39 95d72d892df7fec59107e10914c5729bdf03665f 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b e76375de0bfc9c59bdd91067c901f3eed7d6c8fe 95d72d892df7fec59107e10914c5729bdf03665f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '14', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog -r -2:
  @    95d72d892df7 (8) c_CD0
  |\
  +---o  e76375de0bfc (7) c_CD0
  | | |
  x---+  4535d0af405c (6) c_CD0
  |\| |    split(meta, parent, content) as 95d72d892df7, e76375de0bfc using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  | | |
  | x |  9576e80d6851 (5) c_CD0
  |/ /     rewritten(meta, parent, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  | |      rewritten(meta, parent) as 95d72d892df7 using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  | |
  | x  a0316c4c5417 (4) c_CD0
  |/     rewritten(meta, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  |      meta-changed(meta) as e76375de0bfc using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  49fb7d900906 (3) c_CD0
       meta-changed(meta) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
       split(parent, content) as 9576e80d6851, a0316c4c5417 using split by test (Thu Jan 01 00:00:02 1970 +0000)
  
  $ hg log -G
  @  changeset:   8:95d72d892df7
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   7:e76375de0bfc
  |  parent:      2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

Test rewinding stack
====================

  $ hg clone rewind-testing-base rewind-testing-stack
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-stack

Rewinding the top of the stack only
-----------------------------------

setup
`````

  $ hg up 'desc("c_A0")'
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo AA >> A
  $ hg amend -m 'c_A1'
  1 new orphan changesets
  $ hg evolve --all --update
  move:[2] c_B0
  atop:[3] c_A1
  working directory is now at a65fceb2324a
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog -r 'desc("c_A1")::'
  @  a65fceb2324a (4) c_B0
  |
  | o  d952d1794ff6 (3) c_A1
  | |
  | x  579f120ba918 (1) c_A0
  |      rewritten(description, content) as d952d1794ff6 using amend by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rebased(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   4:a65fceb2324a
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   3:d952d1794ff6
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A1
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'min(desc(c_B0))' --exact
  1 new orphan changesets
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at ac979e0aac4e
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 ac979e0aac4e63ccbbf88ac33942192942302766 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e ac979e0aac4e63ccbbf88ac33942192942302766 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    ac979e0aac4e (5) c_B0
  |\
  | x  a65fceb2324a (4) c_B0
  |/     rewritten(meta, parent) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rebased(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
       meta-changed(meta) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   5:ac979e0aac4e
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: orphan
  |  summary:     c_B0
  |
  | o  changeset:   3:d952d1794ff6
  | |  parent:      0:eba9c2249fe7
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     c_A1
  | |
  x |  changeset:   1:579f120ba918
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 3:d952d1794ff6
  |    summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Testing default argument (and cleanup)
``````````````````````````````````````

rewind with no argument should be equivalent to `--from .`

  $ echo 'default-date = 4 0' >> $HGRCPATH
  $ hg rewind --from '.'
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at a5dd64adbb2a
  $ echo 'default-date = 5 0' >> $HGRCPATH
  $ hg log -G
  @  changeset:   6:a5dd64adbb2a
  |  tag:         tip
  |  parent:      3:d952d1794ff6
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   3:d952d1794ff6
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A1
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 ac979e0aac4e63ccbbf88ac33942192942302766 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e ac979e0aac4e63ccbbf88ac33942192942302766 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e a5dd64adbb2af2e646859b35d0d7128daa73cb2b 4 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  ac979e0aac4e63ccbbf88ac33942192942302766 a5dd64adbb2af2e646859b35d0d7128daa73cb2b 0 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    a5dd64adbb2a (6) c_B0
  |\
  | x  ac979e0aac4e (5) c_B0
  |/|    rewritten(meta, parent) as a5dd64adbb2a using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  | |
  x |  a65fceb2324a (4) c_B0
  |/     meta-changed(meta) as a5dd64adbb2a using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  |      rewritten(meta, parent) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rebased(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
       meta-changed(meta) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  
Automatically rewinding the full stack (with --to)
--------------------------------------------------

  $ hg rewind --hidden --to 'predecessors(.)'
  rewinded to 2 changesets
  (2 changesets obsoleted)
  working directory is now at 3f2d8862657d
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 ac979e0aac4e63ccbbf88ac33942192942302766 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e ac979e0aac4e63ccbbf88ac33942192942302766 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e a5dd64adbb2af2e646859b35d0d7128daa73cb2b 4 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  ac979e0aac4e63ccbbf88ac33942192942302766 a5dd64adbb2af2e646859b35d0d7128daa73cb2b 0 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  579f120ba91885449adc92eedf48ef3569742cee 9c28b7ed3951fd15b20ab75449c1e0fdec445958 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  ac979e0aac4e63ccbbf88ac33942192942302766 3f2d8862657d20af331f0c0531f5228eef4d36c5 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  a5dd64adbb2af2e646859b35d0d7128daa73cb2b 3f2d8862657d20af331f0c0531f5228eef4d36c5 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  d952d1794ff657f5c2a82225d2e6307ed930b32f 9c28b7ed3951fd15b20ab75449c1e0fdec445958 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '11', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    3f2d8862657d (8) c_B0
  |\
  x |  a5dd64adbb2a (6) c_B0
  |\|    rewritten(meta, parent) as 3f2d8862657d using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |
  | x  ac979e0aac4e (5) c_B0
  |/|    rewritten(meta, parent) as 3f2d8862657d using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |    rewritten(meta, parent) as a5dd64adbb2a using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  | |
  x |  a65fceb2324a (4) c_B0
  |/     meta-changed(meta) as a5dd64adbb2a using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  |      rewritten(meta, parent) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rebased(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
       meta-changed(meta) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   8:3f2d8862657d
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   7:9c28b7ed3951
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Automatically rewinding the full stack (with --from)
----------------------------------------------------

  $ echo 'default-date = 6 0' >> $HGRCPATH
  $ hg rewind --hidden --from '.'
  rewinded to 2 changesets
  (2 changesets obsoleted)
  working directory is now at d36d6d267714
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 ac979e0aac4e63ccbbf88ac33942192942302766 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e ac979e0aac4e63ccbbf88ac33942192942302766 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e a5dd64adbb2af2e646859b35d0d7128daa73cb2b 4 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  ac979e0aac4e63ccbbf88ac33942192942302766 a5dd64adbb2af2e646859b35d0d7128daa73cb2b 0 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  579f120ba91885449adc92eedf48ef3569742cee 9c28b7ed3951fd15b20ab75449c1e0fdec445958 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  ac979e0aac4e63ccbbf88ac33942192942302766 3f2d8862657d20af331f0c0531f5228eef4d36c5 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  a5dd64adbb2af2e646859b35d0d7128daa73cb2b 3f2d8862657d20af331f0c0531f5228eef4d36c5 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  d952d1794ff657f5c2a82225d2e6307ed930b32f 9c28b7ed3951fd15b20ab75449c1e0fdec445958 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '11', 'operation': 'rewind', 'user': 'test'}
  d952d1794ff657f5c2a82225d2e6307ed930b32f fef4355b4cc9e2d3ddc154f60e4f4f1a286e9ce7 4 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  a5dd64adbb2af2e646859b35d0d7128daa73cb2b d36d6d267714108384f31762b6193c32f9f97514 4 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  3f2d8862657d20af331f0c0531f5228eef4d36c5 d36d6d267714108384f31762b6193c32f9f97514 0 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '6', 'operation': 'rewind', 'user': 'test'}
  9c28b7ed3951fd15b20ab75449c1e0fdec445958 fef4355b4cc9e2d3ddc154f60e4f4f1a286e9ce7 0 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '11', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    d36d6d267714 (10) c_B0
  |\
  x |  3f2d8862657d (8) c_B0
  |\|    rewritten(meta, parent) as d36d6d267714 using rewind by test (Thu Jan 01 00:00:06 1970 +0000)
  | |
  | x  a5dd64adbb2a (6) c_B0
  |/|    rewritten(meta, parent) as 3f2d8862657d using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |    rewritten(meta, parent) as d36d6d267714 using rewind by test (Thu Jan 01 00:00:06 1970 +0000)
  | |
  x |  ac979e0aac4e (5) c_B0
  |\|    rewritten(meta, parent) as 3f2d8862657d using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |    rewritten(meta, parent) as a5dd64adbb2a using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  | |
  | x  a65fceb2324a (4) c_B0
  |/     meta-changed(meta) as a5dd64adbb2a using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  |      rewritten(meta, parent) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rebased(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
       meta-changed(meta) as ac979e0aac4e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   10:d36d6d267714
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   9:fef4355b4cc9
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A1
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

Merge commits
=============

  $ hg clone -q rewind-testing-base rewind-merge
  $ cd rewind-merge

  $ hg up --clean .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo foo > foo
  $ hg ci -qAm foo

  $ hg merge
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m merge
  $ hg st --change .
  A B

  $ echo bar > foo
  $ hg amend -m 'merge, but foo is now bar'
  $ hg st --change .
  M foo
  A B

  $ hg rewind --from .
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at 9d325190bd87
  $ hg st --change .
  A B

  $ hg glf -r '. + allpredecessors(.) + parents(.)' --hidden
  @    6: merge ()
  |\
  +---x  5: merge, but foo is now bar (foo)
  | |/
  +---x  4: merge ()
  | |/
  | o  3: foo (foo)
  | |
  | ~
  o  2: c_B0 (B)
  |
  ~

  $ cd ..

Rewind --keep
=============

  $ hg init rewind-keep
  $ cd rewind-keep
  $ echo root > root
  $ hg ci -qAm 'root'

  $ echo apple > a
  $ echo banana > b
  $ hg ci -qAm initial

  $ hg rm b
  $ echo apricot > a
  $ echo coconut > c
  $ hg add c
  $ hg status
  M a
  A c
  R b
  $ hg amend -m amended
  $ hg glf --hidden
  @  2: amended (a c)
  |
  | x  1: initial (a b)
  |/
  o  0: root (root)
  

Clean wdir

  $ hg rewind --keep --to 'desc("initial")' --hidden
  rewinded to 1 changesets
  (1 changesets obsoleted)
  $ hg obslog
  @    b4c97fddc16a (3) initial
  |\
  x |  2ea5be2f8751 (2) amended
  |/     rewritten(description, meta, content) as b4c97fddc16a using rewind by test (Thu Jan 01 00:00:06 1970 +0000)
  |
  x  30704102d912 (1) initial
       rewritten(description, content) as 2ea5be2f8751 using amend by test (Thu Jan 01 00:00:06 1970 +0000)
       meta-changed(meta) as b4c97fddc16a using rewind by test (Thu Jan 01 00:00:06 1970 +0000)
  
  $ hg glf --hidden
  @  3: initial (a b)
  |
  | x  2: amended (a c)
  |/
  | x  1: initial (a b)
  |/
  o  0: root (root)
  
  $ hg st
  M a
  A c
  R b

Making wdir even more dirty

  $ echo avocado > a
  $ echo durian > d
  $ hg st
  M a
  A c
  R b
  ? d

No rewinding without --keep

  $ hg rewind --to 'desc("amended")' --hidden
  abort: uncommitted changes
  [255]

XXX: Unfortunately, even with --keep it's not allowed

  $ hg rewind --keep --to 'desc("amended")' --hidden
  abort: uncommitted changes
  [255]
