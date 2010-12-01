#!/bin/sh

echo "The default VM password is demo"

#sudo aptitude install archivematica-shotgun
cat << !
Is this checkout from...
1. amos (need login/password, read write)
2. googlecode (public, read only)
q. Quit
!

echo -n " Your choice? : "
read choice

case $choice in
1) svnRepo="http://amos.artefactual.com/svn/archivematica/trunk" ;;
2) svnRepo="http://code.google.comBLagFIXME" ;;
q) exit ;;
*) echo "\"$choice\" is not valid "; sleep 2 ;;
esac

svn co "$svnRepo" archivematica-trunk

#Create archivematica User for daemons, add demo user to group
##!!!Some of this belongs in the installer for the MCP client & server
sudo adduser --uid 333 --group --system --no-create-home --disabled-login archivematica
sudo gpasswd -a demo archivematica

#Configure sudoers for mcp and client
sudo echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod,/usr/bin/unoconv" >> /etc/sudoers


#check depends
sudo apt-get install libapache2-mod-wsgi python-django python-django-doc python-twisted python-pyinotify ffmpeg2theora libavcodec-unstripped-52 flashplugin-installer unoconv openjdk-6-jre openoffice.org openoffice.org-java-common detox libnotify-bin uuid httrack sendemail curl clamav incron nfs-common flac md5deep ffmpeg winff firebug imagemagick libapache2-mod-php5 mysql-server php5-cli php5-mysql php5-xsl subversion-tools par2 unrar p7zip-full python-execnet digikam kipi-plugins python-mysqldb nfs-kernel-server python-lxml bagit droid fits jhove xena

svnDir="archivematica-trunk/"

lib="/usr/lib/archivematica"
sudo mkdir $lib
etc="/etc/archivematica"
sudo mkdir $etc

sudo ln -s "${svnDir}src/MCPServer/etc" "${etc}/MCPServer"
sudo ln -s "${svnDir}src/MCPClient/etc" "${etc}/MCPClient"
sudo ln -s "${svnDir}src/transcoder/etc" "/etc/transcoder"


sudo ln -s "${svnDir}src/MCPServer/lib/" "${lib}/MCPServer"
sudo ln -s "${svnDir}src/MCPClient/lib/" "${lib}/MCPClient"
sudo ln -s "${svnDir}src/transcoder/lib/" "/usr/lib/transcoder"
sudo ln -s "${svnDir}src/easy-extract/lib/" "/usr/lib/easy-extract"
sudo ln -s "${svnDir}src/dashboard/src/" "/var/www/dashboard"

sudo cp "${svnDir}buildVM/includes/apache.default" "/etc/apache2/sites-available/default"

sudo ln "${svnDir}src/MCPServer/runArchivematicaMCPServer.sh" "/usr/bin/"
sudo ln "${svnDir}src/MCPClient/runArchivematicaMCPClient.sh" "/usr/bin/"
sudo ln "${svnDir}src/easy-extract/bin/easy-extract" "/usr/bin/"
sudo ln "${svnDir}src/transcoder/bin/transcoder" "/usr/bin/"

sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "${lib}/MCPServer"
sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "${lib}/MCPClient"
sudo ln "${svnDir}src/loadConfig/lib/archivematicaLoadConfig.py" "/usr/lib/transcoder"

sudo mkdir /var/archivematica/
sudo ln -s "${svnDir}src/MCPServer/sharedDirectoryStructure" "/var/archivematica/sharedDirectory"
sudo chown -R archivematica:archivematica "/var/archivematica/sharedDirectory"
sudo chmod -R g+s "/var/archivematica/sharedDirectory"


sudo cp  apache.default /etc/apache2/sites-available/default
#xfce4 configuration
cp ./xfceCustomization/gtk-bookmarks /home/demo/.gtk-bookmarks

#cd postBuildRunAssistScripts
./preMCPLogging.sh
sudo mysqladmin create ica-atom
sudo mysqladmin create dcb
sudo mysqladmin create qubit
sudo mysqladmin create dashboard

#fix permissions 
chmod 444 /home/demo/.config/xfce4/panel
chown -R demo:demo /home/demo
chown -R demo:demo /home/demo/.mozilla

sudo chmod 444 -R ~/.config/xfce4/panel
sudo chmod 770 -R  /var/archivematica/sharedDirectory/
sudo chown -R archivematica:archivematica /var/archivematica/sharedDirectory/
sudo chmod -R g+s /var/archivematica/sharedDirectory/
echo "Disabling Screen Saver (Better for VM's)"
sudo aptitude remove xscreensaver
echo " "
echo "===PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS==="
echo " "
sleep 3

