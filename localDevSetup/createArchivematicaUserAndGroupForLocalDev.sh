#Create archivematica User for daemons, add demo user to group
##!!!Some of this belongs in the installer for the MCP client & server
sudo adduser --uid 333 --group --system --home /var/lib/archivematica/ archivematica
echo -n " Your username? : "
read username
sudo gpasswd -a $username archivematica
sudo gpasswd -a clamav archivematica

#TODO
#add current user to archivematica Group

