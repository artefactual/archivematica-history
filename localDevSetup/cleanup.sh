sudo rm /usr/lib/transcoder/archivematicaLoadConfig.py
sudo rm /usr/lib/archivematica/MCPServer/archivematicaLoadConfig.py
sudo rm /usr/lib/archivematica/MCPClient/archivematicaLoadConfig.py

sudo rm /usr/share/fits/xml/fits.xml
sudo mv /usr/share/fits/xml/fits.xml.backup /usr/share/fits/xml/fits.xml


sudo rm -r /usr/lib/archivematica
sudo rm -r /etc/archivematica
sudo rm -r /usr/share/archivematica

sudo rm /usr/bin/runArchivematicaMCPServer.sh 
sudo rm /usr/bin/runArchivematicaMCPClient.sh
sudo rm /usr/bin/upload-qubit 
sudo rm /usr/bin/easy-extract
sudo rm /usr/bin/transcoder
#sudo rm /usr/bin/archivematicaCreateDublincore
sudo rm /usr/bin/archivematicaCreateMD5
sudo rm /usr/bin/archivematicaRestructureForCompliance
sudo rm /usr/bin/sanitizeNames
sudo rm /usr/bin/createDublinCore
sudo rm "/etc/init.d/archivematica-mcp-serverd"
sudo rm "/etc/init.d/archivematica-mcp-clientd"
sudo rm "/etc/init.d/openOfficed"

sudo rm -r /usr/lib/transcoder
sudo rm -r /usr/lib/createDublinCore
sudo rm -r /usr/lib/sanitizeNames
sudo rm -r /etc/transcoder
sudo rm -r /usr/lib/easy-extract

sudo rm -r /var/archivematica/

#sudo mv /etc/apache2/sites-available/default{.dist,}
