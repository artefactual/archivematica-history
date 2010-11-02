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
chmod -R 777 $/etc/apt/sources.list
cp /etc/apt/sources.list $1/etc/apt/sources.list.bak
sed -i -e "s/# deb/deb/g" $1/etc/apt/sources.list
sed -i -e "s/localhost:9999/archive.ubuntu.com/g" $1/etc/apt/sources.list
sed -i -e "s/127.0.0.1:9999/archive.ubuntu.com/g" $1/etc/apt/sources.list
echo "deb http://archive.ubuntu.com/ubuntu/ karmic-proposed main restricted universe multiverse" >> $1/etc/apt/sources.list
chroot $1 aptitude update


#Create archivematica User for daemons, add demo user to group
##!!!Some of this belongs in the installer for the MCP client & server
chroot $1 adduser --uid 333 --group --system --no-create-home --disabled-login archivematica
chroot $1 sudo gpasswd -a demo archivematica
chroot $1 update-python-modules

#Configure sudoers for mcp and client
echo "archivematica ALL=NOPASSWD:/bin/mv,/bin/chown,/bin/chmod" >> $1/etc/sudoers

#Install externals/archivematica
chroot $1 mkdir -p /home/demo/Desktop
svn export includes/.mozilla $1/home/demo/.mozilla
svn export includes/Docs $1/home/demo/Docs
svn export enviromentConfigFiles/exports $1/etc/exports
chroot $1 ln -s /home/demo/Docs /home/demo/Desktop

#setup unonconv service
cp -rf includes/unoconv-listen $1/etc/init.d/unoconv-listen
chroot $1 chmod +x /etc/init.d/unoconv-listen
chroot $1 /usr/sbin/update-rc.d unoconv-listen defaults
chroot $1 chmod -R 770 /home/demo/.mozilla
#chroot $1 mkdir -p /home/demo/.gnome2/nautilus-scripts

svn export includes/sampledata $1/home/demo/testFiles

#XFCE configuration
chroot $1 mkdir /home/demo/.config
chroot $1 mkdir /home/demo/.config/Thunar
chroot $1 mkdir /home/demo/.config/autostart
chroot $1 mkdir -p /home/demo/.config/xfce4/desktop
chroot $1 mkdir -p /home/demo/.config/xfce4/panel

#add archivematica/dashboard icons
cp includes/desktopShortcuts/dashboard-desktop-icon.png $1/usr/share/icons
cp includes/desktopShortcuts/dcb-desktop-icon.png $1/usr/share/icons
cp includes/desktopShortcuts/ica-atom-desktop-icon.png $1/usr/share/icons
cp includes/desktopShortcuts/archivematica-xubuntu-steel.png $1/usr/share/xfce4/backdrops/xubuntu-karmic.png
cp includes/desktopShortcuts/ica-atom.desktop $1/home/demo/Desktop
#cp includes/droid.desktop $1/home/demo/Desktop
#cp includes/jhove.desktop $1/home/demo/Desktop
cp includes/desktopShortcuts/dcb.desktop $1/home/demo/Desktop
#cp includes/dashboard.desktop $1/home/demo/Desktop
#cp includes/WinFF.desktop $1/home/demo/Desktop
cp includes/desktopShortcuts/Terminal.desktop $1/home/demo/Desktop

#add launcher scripts
cp includes/desktopShortcuts/runica-atom.sh $1/usr/bin
cp includes/desktopShortcuts/rundcb.sh $1/usr/bin
cp includes/desktopShortcuts/rundashboard.sh $1/usr/bin
cp includes/desktopShortcuts/runjhove.sh $1/usr/bin

#xfce4 configuration
cp includes/panel/* $1/home/demo/.config/xfce4/panel
cp includes/xfceCustomization/xfce4-desktop.xml $1/etc/xdg/xubuntu/xfce4/xfconf/xfce-perchannel-xml
cp includes/xfceCustomization/xfce4-session.xml $1/etc/xdg/xubuntu/xfce4/xfconf/xfce-perchannel-xml
cp includes/xfceCustomization/icons.screen0.rc $1/home/demo/.config/xfce4/desktop
cp includes/xfceCustomization/user-dirs.defaults $1/etc/xdg
cp includes/xfceCustomization/uca.xml $1/home/demo/.config/Thunar
cp includes/xfceCustomization/thunarrc $1/home/demo/.config/Thunar
cp includes/xfceCustomization/thunar.desktop $1/home/demo/.config/autostart
cp includes/xfceCustomization/gtk-bookmarks $1/home/demo/.gtk-bookmarks
cp includes/xfceCustomization/gdm.custom.conf $1/etc/gdm/custom.conf

#fix permissions 
chroot $1 chmod 444 /home/demo/.config/xfce4/panel
chroot $1 chown -R demo:demo /home/demo
chroot $1 chown -R demo:demo /home/demo/.mozilla


