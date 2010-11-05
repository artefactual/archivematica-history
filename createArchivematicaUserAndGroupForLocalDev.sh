#Create archivematica User for daemons, add demo user to group
##!!!Some of this belongs in the installer for the MCP client & server
sudo adduser --uid 333 --group --system --no-create-home --disabled-login archivematica
sudo gpasswd -a demo archivematica

#Configure sudoers for mcp and client
sudo echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod" >> /etc/sudoers


#TODO
#add current user to archivematica Group

