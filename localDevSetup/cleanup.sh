sudo rm /usr/share/fits/xml/fits.xml
sudo mv /usr/share/fits/xml/fits.xml.backup /usr/share/fits/xml/fits.xml


sudo rm -r /usr/lib/archivematica
sudo rm -r /etc/archivematica
sudo rm -r /usr/share/archivematica

sudo rm /usr/bin/upload-qubit 
sudo rm /usr/bin/easy-extract
sudo rm /usr/bin/transcoder
#sudo rm /usr/bin/archivematicaCreateDublincore
sudo rm /usr/bin/archivematicaCreateMD5
sudo rm /usr/bin/archivematicaRestructureForCompliance
sudo rm /usr/bin/sanitizeNames
sudo rm /usr/bin/createDublinCore


sudo rm -r /usr/lib/createDublinCore
sudo rm -r /usr/lib/sanitizeNames
sudo rm -r /usr/lib/easy-extract

sudo rm -r /var/archivematica/

#sudo mv /etc/apache2/sites-available/default{.dist,}


# These are disabled because: upstart fails to recognize the service if they are enabled
#sudo rm "/etc/init/archivematica-mcp-server.conf"
#sudo rm "/etc/init/archivematica-mcp-client.conf"
#sudo rm "/etc/init/openoffice-service.conf"