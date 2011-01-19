set +e
origDir="`pwd`/"
cd ../
svnDir="`pwd`/"

lib="/usr/lib/archivematica"
sudo mkdir $lib
etc="/etc/archivematica"
sudo mkdir $etc

sudo ln -s "${svnDir}src/MCPServer/etc" "${etc}/MCPServer"
sudo ln -s "${svnDir}src/MCPClient/etc" "${etc}/MCPClient"
sudo ln -s "${svnDir}src/SIPCreationTools/etc/" "${etc}/SIPCreationTools"
sudo ln -s "${svnDir}src/transcoder/etc" "/etc/transcoder"


sudo ln -s "${svnDir}src/MCPServer/lib/" "${lib}/MCPServer"
sudo ln -s "${svnDir}src/MCPClient/lib/" "${lib}/MCPClient"
sudo ln -s "${svnDir}src/SIPCreationTools/lib/" "${lib}/SIPCreationTools"
sudo ln -s "${svnDir}src/upload-qubit/lib/" "${lib}/upload-qubit"
sudo ln -s "${svnDir}src/transcoder/lib/" "/usr/lib/transcoder"
sudo ln -s "${svnDir}src/easy-extract/lib/" "/usr/lib/easy-extract"
sudo ln -s "${svnDir}src/sanitizeNames/lib/" "/usr/lib/sanitizeNames"
sudo ln -s "${svnDir}src/dashboard/src/" "/usr/local/share/dashboard"
sudo ln -s "${svnDir}src/createDublinCore/lib/" "/usr/lib/createDublinCore"

sudo ln "${svnDir}src/MCPServer/runArchivematicaMCPServer.sh" "/usr/bin/"
sudo ln "${svnDir}src/MCPClient/runArchivematicaMCPClient.sh" "/usr/bin/"
#sudo ln "${svnDir}src/SIPCreationTools/bin/archivematicaCreateDublincore" "/usr/bin/"
sudo ln "${svnDir}src/createDublinCore/bin/createDublinCore" "/usr/bin/"
sudo ln "${svnDir}src/SIPCreationTools/bin/archivematicaCreateMD5" "/usr/bin/"
sudo ln "${svnDir}src/SIPCreationTools/bin/archivematicaRestructureForCompliance" "/usr/bin/"

sudo ln "${svnDir}src/upload-qubit/upload-qubit" "/usr/bin/" 
sudo ln "${svnDir}src/easy-extract/bin/easy-extract" "/usr/bin/"
sudo ln "${svnDir}src/transcoder/bin/transcoder" "/usr/bin/"
sudo ln "${svnDir}src/sanitizeNames/bin/sanitizeNames" "/usr/bin/"

sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "${lib}/MCPServer"
sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "${lib}/MCPClient"
sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "/usr/lib/transcoder"

sudo mkdir /var/archivematica/
sudo ln -s "${svnDir}src/MCPServer/sharedDirectoryStructure" "/var/archivematica/sharedDirectory"
sudo chown -R archivematica:archivematica "/var/archivematica/sharedDirectory"
sudo chmod -R g+s "/var/archivematica/sharedDirectory"


echo setting permission on share directories
sudo chmod -R 777 /var/archivematica/sharedDirectory/
echo restarting apache
sudo apache2ctl restart

#Configure sudoers for mcp and client
echo about to edit sudoers file
set -e
cd "$origDir"
tmp="./sudoers-`uuid`"
sudo cp /etc/sudoers "./ETCsudoersBackup-`date`"
sudo grep -v archivematica  "/etc/sudoers" > "${tmp}"
sudo echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod,/usr/bin/unoconv,/usr/bin/gs,/usr/lib/transcoder/transcoderScripts/DocumentConverter.py" >> "${tmp}"
sudo chown 0:0 "${tmp}"
sudo chmod 440 "${tmp}"
sudo mv -f "${tmp}" /etc/sudoers
echo sudoers file was edited


