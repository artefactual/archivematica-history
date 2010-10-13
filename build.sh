#!/bin/sh
#This script  will be modified to allow user to select the type of vm to build.
rootSize="8000"
cat << !
Build Archivematica VM
1. KVM
2. vmware
3. xen
q. Quit
!

echo -n " Your choice? : "
read choice

case $choice in
1) vmType="kvm" ;;
2) vmType="vmserver" ;;
3) vmType="xen" ;;
q) exit ;;
*) echo "\"$choice\" is not valid "; sleep 2 ;;
esac

svnRev=`svn info . |grep '^Revision: '|sed 's/Revision: //g'`

sudo vmbuilder "$vmType" ubuntu \
-c archivematica.cfg \
-d "archivematicaBuild-${svnRev}" \
--rootsize ${rootSize} \
--execscript "`pwd`/archivematica.sh" \
--hostname "Archivematica-${svnRev}"
