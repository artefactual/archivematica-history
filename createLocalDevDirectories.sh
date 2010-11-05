svnDir="`pwd`/"
sudo ln -s "${svnDir}src/MCPServer/etc" "/etc/archivematicaMCPServer"
sudo ln -s "${svnDir}src/MCPClient/etc" "/etc/archivematicaMCPClient"
sudo ln -s "${svnDir}src/transcoder/etc" "/etc/transcoder"

lib="/usr/lib/archivematica"
sudo mkdir $lib

sudo ln -s "${svnDir}src/MCPServer/lib/" "${lib}/MCPServer"
sudo ln -s "${svnDir}src/MCPClient/lib/" "${lib}/MCPClient"
sudo ln -s "${svnDir}src/transcoder/lib/" "/usr/lib/transcoder"

sudo ln "${svnDir}src/MCPServer/runArchivematicaMCPServer.sh" "/usr/bin/"
sudo ln "${svnDir}src/MCPClient/runArchivematicaMCPClient.sh" "/usr/bin/"

sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "${lib}/MCPServer"
sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "${lib}/MCPClient"
sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "/usr/lib/transcoder"

sudo mkdir /var/archivematica/
sudo ln -s "${svnDir}src/MCPServer/sharedDirectoryStructure" "/var/archivematica/sharedDirectory"

