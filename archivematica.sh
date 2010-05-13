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


#Prepare Ubuntu
chroot $1 chmod -R 777 /etc/apt/sources.list
chroot $1 cp /etc/apt/sources.list /etc/apt/sources.list.bak
chroot $1 sed -i -e "s/# deb/deb/g" /etc/apt/sources.list
chroot $1 sed -i -e "s/localhost:9999/archive.ubuntu.com/g" /etc/apt/sources.list
chroot $1 sed -i -e "s/127.0.0.1:9999/archive.ubuntu.com/g" /etc/apt/sources.list
echo "deb http://archive.ubuntu.com/ubuntu/ karmic-proposed main restricted universe multiverse" >> $1/etc/apt/sources.list
chroot $1 aptitude update
#chroot $1 aptitude -q -Ry build-dep -d openjdk-6-jre jacksum openoffice.org-java-common
#chroot $1 aptitude -t jaunty-proposed install openjdk-6-jre jacksum openoffice.org-java-common
chroot $1 rm -rf /home/demo/Documents
chroot $1 rm -rf /home/demo/Music
chroot $1 rm -rf /home/demo/Pictures
chroot $1 rm -rf /home/demo/Public
chroot $1 rm -rf /home/demo/Templates
chroot $1 rm -rf /home/demo/Videos

#Install externals/archivematica
chroot $1 mkdir -p /home/demo/Desktop
chroot $1 mkdir /var/7-storeAIP
chroot $1 ln -s /var/7-storeAIP/ /home/demo
svn export includes/sampledata $1/home/demo/testFiles
svn export includes/externals $1/opt/externals
svn export includes/archivematica $1/opt/archivematica
svn export includes/.mozilla $1/home/demo/.mozilla
svn export includes/xenaconfig $1/home/demo/.java
svn export includes/Docs $1/home/demo/Docs
chroot $1 ln -s /home/demo/Docs /home/demo/Desktop
cp -rf includes/cron.tab $1/etc/cron.tab
chroot $1 crontab -u demo /etc/cron.tab
cp -rf includes/incron.allow $1/etc/incron.allow
cp -rf includes/incron.tab $1/etc/incron.tab
chroot $1 incrontab /etc/incron.tab
chroot $1 chmod -R 770 /home/demo/.mozilla
chroot $1 mkdir -p /home/demo/.gnome2/nautilus-scripts
chroot $1 mkdir /home/demo/1-receiveSIP
chroot $1 mkdir /home/demo/2-reviewSIP
chroot $1 mkdir /home/demo/3-quarantineSIP
chroot $1 mkdir /home/demo/4-appraiseSIP
chroot $1 mkdir /home/demo/5-prepareAIP
chroot $1 mkdir /home/demo/6-reviewAIP	
chroot $1 mkdir /home/demo/8-reviewDIP
chroot $1 mkdir /home/demo/9-uploadDIP
chroot $1 mkdir /home/demo/ingestLogs
chroot $1 mkdir /home/demo/SIPerrors
chroot $1 mkdir /home/demo/SIPerrors/normalizationErrors
chroot $1 mkdir /home/demo/SIPerrors/possibleVirii
chroot $1 mkdir /home/demo/SIPerrors/rejectedSIPs
chroot $1 mkdir /home/demo/.config
chroot $1 mkdir /home/demo/.config/Thunar
chroot $1 mkdir /home/demo/.config/autostart
chroot $1 mkdir -p /home/demo/.config/xfce4/desktop
chroot $1 mkdir -p /home/demo/.config/xfce4/panel

#Gnome Integration/Customization
cp -p includes/makeMD5 $1/home/demo/.gnome2/nautilus-scripts
cp -p includes/checkMD5 $1/home/demo/.gnome2/nautilus-scripts
cp -p includes/Bagit $1/home/demo/.gnome2/nautilus-scripts
cp -p includes/bagcheck $1/home/demo/.gnome2/nautilus-scripts
cp includes/dashboard-desktop-icon.png $1/usr/share/icons
cp includes/dcb-desktop-icon.png $1/usr/share/icons
cp includes/ica-atom-desktop-icon.png $1/usr/share/icons
cp includes/archivematica-xubuntu-steel.png $1/usr/share/xfce4/backdrops/xubuntu-karmic.png

cp includes/ica-atom.desktop $1/home/demo/Desktop
cp includes/droid.desktop $1/home/demo/Desktop
cp includes/jhove.desktop $1/home/demo/Desktop
cp includes/NLNZ-metadata-extractor.desktop $1/home/demo/Desktop
#cp includes/xena.desktop $1/home/demo/Desktop
#cp includes/view.desktop $1/home/demo/Desktop
cp includes/dcb.desktop $1/home/demo/Desktop
#cp includes/dashboard.desktop $1/home/demo/Desktop
cp includes/WinFF.desktop $1/home/demo/Desktop
cp includes/Terminal.desktop $1/home/demo/Desktop
cp includes/rundroid.sh $1/usr/bin
cp includes/runica-atom.sh $1/usr/bin
cp includes/rundcb.sh $1/usr/bin
cp includes/rundashboard.sh $1/usr/bin
cp includes/runjhove.sh $1/usr/bin
#cp includes/runxena.sh $1/usr/bin
#cp includes/runview.sh $1/usr/bin

#xfce4 configuration
cp includes/panel/* $/home/demo/.config/xfce4/panel
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
chroot $1 chmod 444 /home/demo/.config/xfce4/panel/*
chroot $1 chown -R demo:demo /home/demo
chroot $1 chown -R demo:demo /home/demo/.mozilla
chroot $1 chown -R demo:demo /opt/externals
chroot $1 chown -R demo:demo /var/7-storeAIP

#Begin Qubit Configuration
chroot $1 /etc/init.d/mysql start
chroot $1 mysqladmin create qubit
chroot $1 mysqladmin create icaatom
chroot $1 mysqladmin create dcb
chroot $1 mysqladmin create dashboard
cp includes/php.ini $1/etc/php5/cli
cp includes/php.ini $1/etc/php5/apache2
cp includes/apache.default $1/etc/apache2/sites-available/default
chroot $1 apache2ctl restart
svn checkout http://qubit-toolkit.googlecode.com/svn/branches/ica-atom  ica-atom-svn
svn checkout http://qubit-toolkit.googlecode.com/svn/branches/dcb  dcb-svn
svn checkout http://qubit-toolkit.googlecode.com/svn/trunk  qubit-svn
svn export ica-atom-svn $1/var/www/ica-atom
svn export dcb-svn $1/var/www/dcb
svn export qubit-svn $1/var/www/qubit

apache2ctl restart
chroot $1 chown -R www-data:www-data /var/www/ica-atom
chroot $1 chown -R www-data:www-data /var/www/dcb
chroot $1 chown -R www-data:www-data /var/www/qubit
chroot $1 sh -c 'echo EnableSendfile Off >> /etc/apache2/apache2.conf'
chroot $1 a2enmod rewrite

