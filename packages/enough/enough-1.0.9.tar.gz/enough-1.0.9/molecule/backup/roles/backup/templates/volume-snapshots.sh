#!/bin/bash

source /usr/lib/backup/openrc.sh

for volume in $(openstack ${OS_INSECURE} volume list --column Name --format value) ; do
    openstack ${OS_INSECURE} volume snapshot create --force --volume $volume $(date +%Y-%m-%d)-$volume
done
