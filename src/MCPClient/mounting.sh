server=asspire.local
#remotely: chmod 666 directory
#put host file entry into /etc/hosts 192.168.1.105 
#/etc/exports/
##/var/archivematica/ *(rw,no_root_squash,no_subtree_check,anonuid=1000,anongid=1000,insecure)
##/home/joseph/archivematica/src/MCPServer/sharedDirectoryStructure/  *(rw,no_root_squash,no_subtree_check,anonuid=1000,anongid=1000,insecure)
#fileLocation="/var/archivematica/"
shareLocation="/home/joseph/archivematica/src/MCPServer/sharedDirectoryStructure/sharedDirectoryStructure/"
sudo mount "${server}:${shareLocation}" /var/archivematica/sharedDirectory/
