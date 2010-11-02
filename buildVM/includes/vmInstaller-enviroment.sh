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


#Clean up sources.list remove proxy addresses
chmod -R 777 "$1/etc/apt/sources.list"
cp /etc/apt/sources.list $1/etc/apt/sources.list.bak
sed -i -e "s/# deb/deb/g" "$1/etc/apt/sources.list"
sed -i -e "s/localhost:9999/archive.ubuntu.com/g" "$1/etc/apt/sources.list"
sed -i -e "s/127.0.0.1:9999/archive.ubuntu.com/g" "$1/etc/apt/sources.list"
echo "deb http://archive.ubuntu.com/ubuntu/ karmic-proposed main restricted universe multiverse" >> $1/etc/apt/sources.list
chroot "$1" aptitude update


#Create archivematica User for daemons, add demo user to group
##!!!Some of this belongs in the installer for the MCP client & server
chroot "$1" adduser --uid 333 --group --system --no-create-home --disabled-login archivematica
chroot "$1" sudo gpasswd -a demo archivematica
chroot "$1" update-python-modules

#Configure sudoers for mcp and client
echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod" >> $1/etc/sudoers

#Install externals/archivematica
chroot "$1" mkdir -p /home/demo/Desktop
svn export ./.mozilla $1/home/demo/.mozilla
svn export ./Docs $1/home/demo/Docs
svn export enviromentConfigFiles/exports $1/etc/exports
chroot "$1" ln -s /home/demo/Docs /home/demo/Desktop

#setup unonconv service
cp -rf ./unoconv-listen $1/etc/init.d/unoconv-listen
chroot "$1" chmod +x /etc/init.d/unoconv-listen
chroot "$1" /usr/sbin/update-rc.d unoconv-listen defaults
chroot "$1" chmod -R 770 /home/demo/.mozilla
#chroot "$1" mkdir -p /home/demo/.gnome2/nautilus-scripts

svn export ./sampledata $1/home/demo/testFiles

#XFCE configuration
chroot "$1" mkdir /home/demo/.config
chroot "$1" mkdir /home/demo/.config/Thunar
chroot "$1" mkdir /home/demo/.config/autostart
chroot "$1" mkdir -p /home/demo/.config/xfce4/desktop
chroot "$1" mkdir -p /home/demo/.config/xfce4/panel

#add archivematica/dashboard icons
cp ./desktopShortcuts/dashboard-desktop-icon.png $1/usr/share/icons
cp ./desktopShortcuts/dcb-desktop-icon.png $1/usr/share/icons
cp ./desktopShortcuts/ica-atom-desktop-icon.png $1/usr/share/icons
cp ./desktopShortcuts/archivematica-xubuntu-steel.png $1/usr/share/xfce4/backdrops/xubuntu-karmic.png
cp ./desktopShortcuts/ica-atom.desktop $1/home/demo/Desktop
#cp ./droid.desktop $1/home/demo/Desktop
#cp ./jhove.desktop $1/home/demo/Desktop
cp ./desktopShortcuts/dcb.desktop $1/home/demo/Desktop
#cp ./dashboard.desktop $1/home/demo/Desktop
#cp ./WinFF.desktop $1/home/demo/Desktop
cp ./desktopShortcuts/Terminal.desktop $1/home/demo/Desktop

#add launcher scripts
cp ./desktopShortcuts/runica-atom.sh $1/usr/bin
cp ./desktopShortcuts/rundcb.sh $1/usr/bin
cp ./desktopShortcuts/rundashboard.sh $1/usr/bin
#cp ./desktopShortcuts/runjhove.sh $1/usr/bin

#xfce4 configuration
cp ./panel/* $1/home/demo/.config/xfce4/panel
cp ./xfceCustomization/xfce4-desktop.xml $1/etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ./xfceCustomization/xfce4-session.xml $1/etc/xdg/xdg-xubuntu/xfce4/xfconf/xfce-perchannel-xml/
cp ./xfceCustomization/icons.screen0.rc $1/home/demo/.config/xfce4/desktop
cp ./xfceCustomization/user-dirs.defaults $1/etc/xdg
cp ./xfceCustomization/uca.xml $1/home/demo/.config/Thunar
cp ./xfceCustomization/thunarrc $1/home/demo/.config/Thunar
cp ./xfceCustomization/thunar.desktop $1/home/demo/.config/autostart
cp ./xfceCustomization/gtk-bookmarks $1/home/demo/.gtk-bookmarks
cp ./xfceCustomization/gdm.custom.conf $1/etc/gdm/custom.conf

#fix permissions 
chroot "$1" chmod 444 /home/demo/.config/xfce4/panel
chroot "$1" chown -R demo:demo /home/demo
chroot "$1" chown -R demo:demo /home/demo/.mozilla


