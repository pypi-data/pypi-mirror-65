Booting from a backup
=====================

* Login https://horizon.cloud.ovh.net/
* Pause the broken instance
* Go to Images
* Locate the latest backup
* Launch with the expected flavor and the same name as the broken flavor
* Edit security group, remove default and add the security group that has the same name as the broken instance
* Add the IP of the new instance to /etc/hosts and manually check it can be logged in and responds
* Login the new instance and set /etc/resolv.conf to 8.8.8.8
* Edit hosts.yml and replace the IP of the broken instance with the IP of the new instance
* Run ansible-playbook on the new instance

