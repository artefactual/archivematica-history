#!/bin/bash

# This file is part of Archivematica.
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.


# @package Archivematica
# @subpackage Configuration
# @author Austin Trask <austin@artefactual.com>
# @author Joseph Perry <joseph@artefactual.com>
# @version svn: $Id$

#Create DBs

if [ "$(id -u)" != "0" ]; then
	echo "Sorry, you are not root."
	exit 1
fi

echo "The default password is demo"

stty -echo
read -p "Enter mysql root password[hit Enter if blank]: " dpPassword; echo
stty echo

if [ -n "$dpPassword" ] ; then 
        dpPassword="-p${dpPassword}"
fi

./vmInstaller-mcp-db.sh "$dpPassword"
mysqladmin create ica-atom $dpPassword
mysqladmin create dcb $dpPassword
mysqladmin create qubit $dpPassword
mysqladmin create dashboard $dpPassword

dpPassword=""

cp apache.default /etc/apache2/sites-available/default



#Install externals/archivematica
mkdir -p /home/demo/Desktop
cp -a ./Docs /home/demo/Docs
cp -a enviromentConfigFiles/exports /etc/exports
ln -s /home/demo/Docs /home/demo/Desktop


cp -a ./sampledata /home/demo/testFiles
#cp -a ./postBuildScripts /home/demo/postBuildScripts

#XFCE configuration
mkdir /home/demo/.config
mkdir /home/demo/.config/Thunar
mkdir /home/demo/.config/autostart
mkdir -p /home/demo/.config/xfce4/desktop
mkdir -p /home/demo/.config/xfce4/panel

#add archivematica/dashboard icons
cp ./desktopShortcuts/dashboard-desktop-icon.png /usr/share/icons
cp ./desktopShortcuts/dcb-desktop-icon.png /usr/share/icons
cp ./desktopShortcuts/ica-atom-desktop-icon.png /usr/share/icons
cp ./desktopShortcuts/archivematica-xubuntu-steel.png /usr/share/xfce4/backdrops/xubuntu-karmic.png
cp ./desktopShortcuts/ica-atom.desktop /home/demo/Desktop
cp ./desktopShortcuts/dcb.desktop /home/demo/Desktop
cp ./dashboard.desktop /home/demo/Desktop
cp ./desktopShortcuts/Terminal.desktop /home/demo/Desktop

#add launcher scripts
cp ./desktopShortcuts/runica-atom.sh /usr/bin
cp ./desktopShortcuts/rundcb.sh /usr/bin
cp ./desktopShortcuts/rundashboard.sh /usr/bin


#xfce4 configuration
cp ./panel/* /home/demo/.config/xfce4/panel
cp ./xfceCustomization/xfce4-desktop.xml /etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ./xfceCustomization/xfce4-session.xml /etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ./xfceCustomization/icons.screen0.rc /home/demo/.config/xfce4/desktop
cp ./xfceCustomization/user-dirs.defaults /etc/xdg
cp ./xfceCustomization/uca.xml /home/demo/.config/Thunar
cp ./xfceCustomization/thunarrc /home/demo/.config/Thunar
cp ./xfceCustomization/thunar.desktop /home/demo/.config/autostart
cp ./xfceCustomization/gtk-bookmarks /home/demo/.gtk-bookmarks
cp ./xfceCustomization/gdm.custom.conf /etc/gdm/custom.conf

#fix permissions 
chmod 444 /home/demo/.config/xfce4/panel
chown -R demo:demo /home/demo

./vmInstaller-mcp-db.sh
./vmInstaller-dcb.sh
./vmInstaller-ica-atom.sh
./vmInstaller-qubit.sh

sudo aptitude remove xscreensaver
sudo gpasswd -a demo archivematica
echo " "
echo "===PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS==="
echo " "
sleep 3


