sudo mv /etc/archivematica/archivematicaConfig.conf /etc/archivematica/archivematicaConfig.orig.conf
sudo mv /etc/archivematica/archivematicaConfig-DEV.conf /etc/archivematica/archivematicaConfig.conf
echo -n "checkout as (username): "
read username
svn checkout http://amos.artefactual.com/svn/archivematica/trunk/ --username ${username} ~/archivematica

sudo chmod 777 /usr/bin/runArchivematicaMCPServer.sh
sudo chmod 777 /usr/bin/runArchivematicaMCPClient.sh
sudo echo "sudo -u archivematica ~/archivematica/includes/MCP/MCP/bin/archivematicaMCP.py" > /usr/bin/runArchivematicaMCPServer.sh
sudo echo "sudo -u archivematica ~/archivematica/includes/MCP/client/archivematicaClient.py" > /usr/bin/runArchivematicaMCPClient.sh
sudo chmod 755 /usr/bin/runArchivematicaMCPServer.sh
sudo chmod 755 /usr/bin/runArchivematicaMCPClient.sh

cp /usr/bin/archivematicaLoadConfig.py "/home/demo/archivematica/includes/MCP/client/."
cp /usr/bin/archivematicaLoadConfig.py "/home/demo/archivematica/includes/MCP/MCP/bin/."

sudo chown -R archivematica:archivematica "/home/demo/archivematica/sharedDirectoryStructure"
#sudo chmod 777 "/home/demo/archivematica/sharedDirectoryStructure"

echo ""
echo "done"

