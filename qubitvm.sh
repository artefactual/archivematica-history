#!/bin/bash
#Prepare Ubuntu
chroot $1 chmod -R 777 /etc/apt/sources.list
chroot $1 cp /etc/apt/sources.list /etc/apt/sources.list.bak
chroot $1 sed -i -e "s/# deb/deb/g" /etc/apt/sources.list
chroot $1 sed -i -e "s/localhost:9999/archive.ubuntu.com/g" /etc/apt/sources.list
chroot $1 sed -i -e "s/127.0.0.1:9999/archive.ubuntu.com/g" /etc/apt/sources.list
echo "deb http://archive.ubuntu.com/ubuntu/ jaunty-proposed main restricted universe multiverse" >> $1/etc/apt/sources.list
chroot $1 aptitude update
chroot $1 aptitude -q -Ry build-dep -d openjdk-6-jre jacksum openoffice.org-java-common
chroot $1 aptitude -t jaunty-proposed install openjdk-6-jre jacksum openoffice.org-java-common

#Install OAIS
chroot $1 mkdir /var/archivalstorage
chroot $1 mkdir /var/ingest
#SWITCH TO SVN EXPORT
svn export scripts/sampledata $1/var/sampledata
svn export scripts/OAIS $1/usr/local/OAIS
svn export scripts/.mozilla $1/home/demo/.mozilla
chroot $1 mkdir -p /home/demo/.config/fsniper
cp -rf scripts/fsniper.config $1/home/demo/.config/fsniper/config
#REMOVED fsniper autostart for now
cp -rf scripts/fsniper.init.d $1/etc/init.d/fsniper
chroot $1 chmod +x /etc/init.d/fsniper
chroot $1 update-rc.d fsniper defaults
chroot $1 chmod -R 770 /home/demo/.mozilla
chroot $1 ln -s /var/archivalstorage/ /home/demo
chroot $1 ln -s /var/sampledata/ /home/demo
chroot $1 ln -s /var/ingest/ /home/demo
chroot $1 mkdir -p /home/demo/Desktop
chroot $1 mkdir -p /home/demo/.gnome2/nautilus-scripts
chroot $1 mkdir /home/demo/mybags
chroot $1 mkdir /home/demo/quarantine
chroot $1 mkdir /home/demo/accessionrecords

cp -p scripts/makeMD5 $1/home/demo/.gnome2/nautilus-scripts
cp -p scripts/checkMD5 $1/home/demo/.gnome2/nautilus-scripts
cp -p scripts/Bagit $1/home/demo/.gnome2/nautilus-scripts
cp -p scripts/Accession $1/home/demo/.gnome2/nautilus-scripts
cp scripts/Qubit.png $1/usr/share/icons
cp scripts/ica-atom.desktop $1/home/demo/Desktop
cp scripts/droid.desktop $1/home/demo/Desktop
cp scripts/jhove.desktop $1/home/demo/Desktop
cp scripts/NLNZ-metadata-extractor.desktop $1/home/demo/Desktop
cp scripts/xena.desktop $1/home/demo/Desktop
cp scripts/view.desktop $1/home/demo/Desktop
cp scripts/rundroid.sh $1/usr/bin
cp scripts/runica.sh $1/usr/bin
cp scripts/runjhove.sh $1/usr/bin
cp scripts/runxena.sh $1/usr/bin
cp scripts/runview.sh $1/usr/bin
chroot $1 mkdir /home/demo/xena-output
chroot $1 chown -R demo:demo /home/demo
chroot $1 chown -R demo:demo /home/demo/.mozilla
chroot $1 chown -R demo:demo /usr/local/OAIS
chroot $1 chown -R demo:demo /var/ingest
chroot $1 chown -R demo:demo /var/archivalstorage

#Begin Qubit Configuration
chroot $1 /etc/init.d/mysql start
chroot $1 mysqladmin create qubit
cp scripts/php.ini $1/etc/php5/cli
cp scripts/php.ini $1/etc/php5/apache2
cp scripts/apache.default $1/etc/apache2/sites-available/default
chroot $1 apache2ctl restart
svn checkout http://qubit-toolkit.googlecode.com/svn/tags/release-1.0.7  qubit-svn
svn export qubit-svn $1/var/www/qubit

apache2ctl restart
chroot $1 chown -R www-data:www-data /var/www/qubit
chroot $1 sh -c 'echo EnableSendfile Off >> /etc/apache2/apache2.conf'
chroot $1 a2enmod rewrite

echo Apache is configured and Qubit has been downloaded please finish with the installer!
