#!/bin/bash

mkdir -p ~/.enough/dev
ln -sf ~/.enough/dev/clouds.yml inventory/group_vars/all/clouds.yml
ln -sf ~/.enough/dev/domain.yml inventory/group_vars/all/domain.yml
if ! test -e ~/.enough/dev/domain.yml ; then
    cat > ~/.enough/dev/domain.yml <<EOF
---
domain: enough.community
EOF
fi
