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

includesDir="/usr/share/archivematica/vm-includes/"

${includesDir}vmInstaller-mcp-db.sh "$dpPassword"
mysqladmin create ica-atom $dpPassword
mysqladmin create dcb $dpPassword
mysqladmin create qubit $dpPassword
mysqladmin create dashboard $dpPassword

dpPassword=""

cp ${includesDir}php.ini /etc/php5/cli
cp ${includesDir}php.ini /etc/php5/apache2
cp ${includesDir}apache.default /etc/apache2/sites-available/default



#Install externals/archivematica
mkdir -p /home/demo/Desktop
cp -a ${includesDir}Docs /home/demo/Docs
cp -a enviromentConfigFiles/exports /etc/exports
ln -s /home/demo/Docs /home/demo/Desktop


cp -a ${includesDir}sampledata /home/demo/testFiles
#cp -a ${includesDir}postBuildScripts /home/demo/postBuildScripts

#XFCE configuration
mkdir /home/demo/.config
mkdir /home/demo/.config/Thunar
mkdir /home/demo/.config/autostart
mkdir -p /home/demo/.config/xfce4/desktop
mkdir -p /home/demo/.config/xfce4/panel

#add archivematica/dashboard icons
cp ${includesDir}desktopShortcuts/dashboard-desktop-icon.png /usr/share/icons
cp ${includesDir}desktopShortcuts/dcb-desktop-icon.png /usr/share/icons
cp ${includesDir}desktopShortcuts/ica-atom-desktop-icon.png /usr/share/icons
cp ${includesDir}desktopShortcuts/archivematica-xubuntu-steel.png /usr/share/xfce4/backdrops/xubuntu-karmic.png
cp ${includesDir}desktopShortcuts/ica-atom.desktop /home/demo/Desktop
cp ${includesDir}desktopShortcuts/dcb.desktop /home/demo/Desktop
cp ${includesDir}dashboard.desktop /home/demo/Desktop
cp ${includesDir}desktopShortcuts/Terminal.desktop /home/demo/Desktop

#add launcher scripts
cp ${includesDir}desktopShortcuts/runica-atom.sh /usr/bin
cp ${includesDir}desktopShortcuts/rundcb.sh /usr/bin
cp ${includesDir}desktopShortcuts/rundashboard.sh /usr/bin


#xfce4 configuration
cp ${includesDir}panel/* /home/demo/.config/xfce4/panel
cp ${includesDir}xfceCustomization/xfce4-desktop.xml /etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ${includesDir}xfceCustomization/xfce4-session.xml /etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ${includesDir}xfceCustomization/icons.screen0.rc /home/demo/.config/xfce4/desktop
cp ${includesDir}xfceCustomization/user-dirs.defaults /etc/xdg
cp ${includesDir}xfceCustomization/uca.xml /home/demo/.config/Thunar
cp ${includesDir}xfceCustomization/thunarrc /home/demo/.config/Thunar
cp ${includesDir}xfceCustomization/thunar.desktop /home/demo/.config/autostart
cp ${includesDir}xfceCustomization/gtk-bookmarks /home/demo/.gtk-bookmarks
cp ${includesDir}xfceCustomization/gdm.custom.conf /etc/gdm/custom.conf

#fix permissions 
chmod 444 /home/demo/.config/xfce4/panel
chown -R demo:demo /home/demo

${includesDir}vmInstaller-mcp-db.sh
${includesDir}vmInstaller-dcb.sh
${includesDir}vmInstaller-ica-atom.sh
${includesDir}vmInstaller-qubit.sh

sudo aptitude remove xscreensaver
sudo gpasswd -a demo archivematica
echo " "
echo "===PLEASE REBOOT TO ENABLE NEW GROUP SETTINGS==="
echo " "
sleep 3


