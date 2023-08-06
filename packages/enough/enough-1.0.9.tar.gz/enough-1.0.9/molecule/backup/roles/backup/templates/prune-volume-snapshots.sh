#!/bin/bash

source /usr/lib/backup/openrc.sh

numdays=${1:-30}
stamp1=`date --date "$numdays days ago" '+%s'`
regex="^([0-9]{4}-[0-9]{2}-[0-9]{2}).*$"
openstack ${OS_INSECURE} volume snapshot list -f value -c Name --limit 10000 |
while read snapshot
do
        if [[ $snapshot =~ $regex ]] ; then
                snapshotdate=`echo $snapshot | sed -r "s/$regex/\1/"`
                stamp2=`date --date "$snapshotdate" '+%s'`
                if [[ $stamp1 -ge $stamp2 ]] ; then
                  openstack ${OS_INSECURE} volume snapshot delete $snapshot
                fi
        fi
done
