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
# @version svn: $Id$


#Clean up sources.list remove proxy addresses
chmod -R 777 $/etc/apt/sources.list
cp /etc/apt/sources.list $1/etc/apt/sources.list.bak
sed -i -e "s/# deb/deb/g" $1/etc/apt/sources.list
sed -i -e "s/localhost:9999/archive.ubuntu.com/g" $1/etc/apt/sources.list
sed -i -e "s/127.0.0.1:9999/archive.ubuntu.com/g" $1/etc/apt/sources.list
echo "deb http://archive.ubuntu.com/ubuntu/ karmic-proposed main restricted universe multiverse" >> $1/etc/apt/sources.list
chroot $1 aptitude update

#Remove ubuntu home folder skeleton
chroot $1 rm -rf /home/demo/Documents
chroot $1 rm -rf /home/demo/Music
chroot $1 rm -rf /home/demo/Pictures
chroot $1 rm -rf /home/demo/Public
chroot $1 rm -rf /home/demo/Templates
chroot $1 rm -rf /home/demo/Videos

#Install archivematica
svn export includes/archivematicaUsrBin $1/usr/bin/temp/
mv $1/usr/bin/temp/* $1/usr/bin/
rm -r $1/usr/bin/temp

svn export includes/MCP/client $1/usr/bin/temp/
mv $1/usr/bin/temp/* $1/usr/bin/
rm -r $1/usr/bin/temp

svn export includes/MCP/MCP/bin $1/usr/bin/temp/
mv $1/usr/bin/temp/* $1/usr/bin/
rm -r $1/usr/bin/temp

svn export includes/archivematicaEtc $1/etc/archivematica
svn export includes/archivematicaUsrShare $1/usr/share/
svn export sharedFolderStructure $1/home/demo/sharedFolders
svn export postBuildScripts $1/home/demo/postBuildScripts

svn export includes/MCP/MCP/mcpModulesConfig $1/etc/archivematica/mcpModulesConfig/

mkdir $1/usr/share/archivematica/
svn export includes/MCP/MCP/mcpModules $1/usr/share/archivematica/mcpModules
svn export includes/archivematicaUsrShare/normalizationScripts $1/usr/share/archivematica/normalizationScripts

chroot $1 ln -s /usr/share/archivematica/mcpModules /usr/lib/pymodules/python2.6/.

chroot $1 adduser --home /dev/null --shell /bin/false --no-create-home --disabled-login archivematica
chroot $1 chown -R archivematica:archivematica /home/demo/sharedFolders

chroot $1 update-python-modules

#Install externals/archivematica
chroot $1 mkdir -p /home/demo/Desktop
svn export includes/.mozilla $1/home/demo/.mozilla
svn export includes/xenaconfig $1/home/demo/.java
svn export includes/Docs $1/home/demo/Docs
chroot $1 ln -s /home/demo/Docs /home/demo/Desktop

#cron and incron no longer needed with MCP
#cp -rf includes/cron.tab $1/etc/cron.tab
#chroot $1 crontab -u demo /etc/cron.tab
#cp -rf includes/incron.allow $1/etc/incron.allow
#cp -rf includes/incron.tab $1/etc/incron.tab
#chroot $1 incrontab /etc/incron.tab

#setup unonconv service
cp -rf includes/unoconv-listen $1/etc/init.d/unoconv-listen
chroot $1 chmod +x /etc/init.d/unoconv-listen
chroot $1 /usr/sbin/update-rc.d unoconv-listen defaults
chroot $1 chmod -R 770 /home/demo/.mozilla
chroot $1 mkdir -p /home/demo/.gnome2/nautilus-scripts

#Should we link these to the new shared folder structure?
#chroot $1 mkdir /home/demo/2-reviewSIP
#chroot $1 mkdir /home/demo/3-quarantineSIP
#chroot $1 mkdir /home/demo/4-appraiseSIP
#chroot $1 mkdir /home/demo/5-prepareAIP
#chroot $1 mkdir /home/demo/6-reviewAIP	
#chroot $1 mkdir /home/demo/8-reviewDIP
#chroot $1 mkdir /home/demo/9-uploadDIP
#chroot $1 mkdir /home/demo/ingestLogs
#chroot $1 mkdir /home/demo/SIPerrors
#chroot $1 mkdir /home/demo/SIPerrors/normalizationErrors
#chroot $1 mkdir /home/demo/SIPerrors/possibleVirii
#chroot $1 mkdir /home/demo/SIPerrors/rejectedSIPs
#chroot $1 mkdir /var/7-storeAIP
#chroot $1 mkdir /var/1-receiveSIP
#chroot $1 ln -s /var/7-storeAIP/ /home/demo
#chroot $1 ln -s /var/1-receiveSIP/ /home/demo

#where should these exports go?
svn export includes/sampledata $1/home/demo/testFiles
#svn export includes/sampledata/ImagesSIP $1/var/1-receiveSIP/ImagesSIP
#svn export includes/sampledata/MultimediaSIP $1/var/1-receiveSIP/MultimediaSIP
#svn export includes/sampledata/OfficeDocsSIP $1/var/1-receiveSIP/OfficeDocsSIP

#XFCE configuration
chroot $1 mkdir /home/demo/.config
chroot $1 mkdir /home/demo/.config/Thunar
chroot $1 mkdir /home/demo/.config/autostart
chroot $1 mkdir -p /home/demo/.config/xfce4/desktop
chroot $1 mkdir -p /home/demo/.config/xfce4/panel

#add archivematica/dashboard icons
cp includes/dashboard-desktop-icon.png $1/usr/share/icons
cp includes/dcb-desktop-icon.png $1/usr/share/icons
cp includes/ica-atom-desktop-icon.png $1/usr/share/icons
cp includes/archivematica-xubuntu-steel.png $1/usr/share/xfce4/backdrops/xubuntu-karmic.png
cp includes/ica-atom.desktop $1/home/demo/Desktop
cp includes/droid.desktop $1/home/demo/Desktop
cp includes/jhove.desktop $1/home/demo/Desktop
cp includes/dcb.desktop $1/home/demo/Desktop
#cp includes/dashboard.desktop $1/home/demo/Desktop
cp includes/WinFF.desktop $1/home/demo/Desktop
cp includes/Terminal.desktop $1/home/demo/Desktop

#add launcher scripts
cp includes/runica-atom.sh $1/usr/bin
cp includes/rundcb.sh $1/usr/bin
cp includes/rundashboard.sh $1/usr/bin
cp includes/runjhove.sh $1/usr/bin

#these are now created by their debian packages
#cp includes/runxena.sh $1/usr/bin
#cp includes/runview.sh $1/usr/bin
#cp includes/rundroid.sh $1/usr/bin

#xfce4 configuration
cp includes/panel/* $1/home/demo/.config/xfce4/panel
cp includes/xfce4-desktop.xml $1/etc/xdg/xubuntu/xfce4/xfconf/xfce-perchannel-xml
cp includes/xfce4-session.xml $1/etc/xdg/xubuntu/xfce4/xfconf/xfce-perchannel-xml
cp includes/icons.screen0.rc $1/home/demo/.config/xfce4/desktop
cp includes/user-dirs.defaults $1/etc/xdg
cp includes/uca.xml $1/home/demo/.config/Thunar
cp includes/thunarrc $1/home/demo/.config/Thunar
cp includes/thunar.desktop $1/home/demo/.config/autostart
cp includes/gtk-bookmarks $1/home/demo/.gtk-bookmarks
cp includes/gdm.custom.conf $1/etc/gdm/custom.conf

#fix permissions 
chroot $1 chmod 444 /home/demo/.config/xfce4/panel
chroot $1 chown -R demo:demo /home/demo
chroot $1 chown -R demo:demo /home/demo/.mozilla
chroot $1 chown -R demo:demo /opt/externals
chroot $1 chown -R demo:demo /var/1-receiveSIP
chroot $1 chown -R demo:demo /var/7-storeAIP

#Create MySQL databases 
chroot $1 /etc/init.d/mysql start
chroot $1 mysqladmin create qubit
chroot $1 mysqladmin create icaatom
chroot $1 mysqladmin create dcb
chroot $1 mysqladmin create dashboard

#configure apache/php
cp includes/php.ini $1/etc/php5/cli
cp includes/php.ini $1/etc/php5/apache2
cp includes/apache.default $1/etc/apache2/sites-available/default
chroot $1 sh -c 'echo EnableSendfile Off >> /etc/apache2/apache2.conf'
chroot $1 a2enmod rewrite
chroot $1 apache2ctl restart


#download and export web tools
svn checkout http://qubit-toolkit.googlecode.com/svn/branches/ica-atom  ica-atom-svn
svn checkout http://qubit-toolkit.googlecode.com/svn/branches/dcb  dcb-svn
svn checkout http://qubit-toolkit.googlecode.com/svn/trunk  qubit-svn
svn export ica-atom-svn $1/var/www/ica-atom
svn export dcb-svn $1/var/www/dcb
svn export qubit-svn $1/var/www/qubit
cp includes/dashboard $1/var/www/dashboard

#fix ownership of web apps
chroot $1 chown -R www-data:www-data /var/www/ica-atom
chroot $1 chown -R www-data:www-data /var/www/dcb
chroot $1 chown -R www-data:www-data /var/www/qubit


