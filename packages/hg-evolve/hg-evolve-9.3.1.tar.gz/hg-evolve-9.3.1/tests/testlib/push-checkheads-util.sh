# setup config and various utility to test new heads checks on push

. $TESTDIR/testlib/common.sh

cat >> $HGRCPATH <<EOF
[ui]
# simpler log output
logtemplate ="{node|short} ({phase}){if(topic, "[{topic}]")}: {desc}\n"

[phases]
# non publishing server
publish=False

[extensions]
# we need to strip some changeset for some test cases
strip=
evolve=
EOF

setuprepos() {
    echo creating basic server and client repo
    hg init server
    cd server
    mkcommit root
    hg phase --public .
    mkcommit A0
    cd ..
    hg clone server client

    if [ "$1" = "single-head" ]; then
        echo >> "server/.hg/hgrc" "[experimental]"
        echo >> "server/.hg/hgrc" "# enforce a single name per branch"
        echo >> "server/.hg/hgrc" "single-head-per-branch = yes"

        echo >> "client/.hg/hgrc" "[ui]"
        echo >> "client/.hg/hgrc" "# simpler log output"
        echo >> "client/.hg/hgrc" 'logtemplate = "{node|short} [{branch}{if(topic, ":{topic}")}] ({phase}): {desc}\\n"'
    fi
}
