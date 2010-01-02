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
chroot $1 rm -rf /home/demo/Documents
chroot $1 rm -rf /home/demo/Music
chroot $1 rm -rf /home/demo/Pictures
chroot $1 rm -rf /home/demo/Public
chroot $1 rm -rf /home/demo/Templates
chroot $1 rm -rf /home/demo/Videos

#Install OAIS
chroot $1 mkdir /var/storeAIP
#SWITCH TO SVN EXPORT
svn export scripts/sampledata $1/home/demo/testFiles
svn export scripts/OAIS $1/opt/OAIS
svn export scripts/archivematica $/opt/archivematica
svn export scripts/.mozilla $1/home/demo/.mozilla
cp -rf scripts/cron.tab $1/etc/cron.tab
chroot $1 crontab -u demo /etc/cron.tab
cp -rf scripts/snipemod.sh $1/usr/local/bin/snipemod.sh
cp -rf scripts/incron.allow $1/etc/incron.allow
cp -rf scripts/incron.tab $1/etc/incron.tab
chroot $1 chmod -R 770 /home/demo/.mozilla
chroot $1 ln -s /var/storeAIP/ /home/demo
chroot $1 mkdir -p /home/demo/Desktop
chroot $1 mkdir -p /home/demo/.gnome2/nautilus-scripts
chroot $1 mkdir /home/demo/accessionreports
chroot $1 mkdir /home/demo/receiveAIP
chroot $1 mkdir /home/demo/quarantine
chroot $1 mkdir /home/demo/generateDIP
chroot $1 mkdir /home/demo/generateAIP
chroot $1 mkdir /home/demo/prepareAIP
chroot $1 mkdir /home/demo/possiblevirii
chroot $1 mkdir /home/demo/receiveSIP
chroot $1 mkdir /home/demo/ingestSIP


cp -p scripts/makeMD5 $1/home/demo/.gnome2/nautilus-scripts
cp -p scripts/checkMD5 $1/home/demo/.gnome2/nautilus-scripts
cp -p scripts/Bagit $1/home/demo/.gnome2/nautilus-scripts
cp -p scripts/RemoveWhiteSpace $1/home/demo/.gnome2/nautilus-scripts
cp scripts/Qubit.png $1/usr/share/icons
cp scripts/qubit.desktop $1/home/demo/Desktop
cp scripts/droid.desktop $1/home/demo/Desktop
cp scripts/jhove.desktop $1/home/demo/Desktop
cp scripts/NLNZ-metadata-extractor.desktop $1/home/demo/Desktop
cp scripts/xena.desktop $1/home/demo/Desktop
cp scripts/view.desktop $1/home/demo/Desktop
cp scripts/rundroid.sh $1/usr/bin
cp scripts/runqubit.sh $1/usr/bin
cp scripts/runjhove.sh $1/usr/bin
cp scripts/runxena.sh $1/usr/bin
cp scripts/runview.sh $1/usr/bin
chroot $1 mkdir /home/demo/xena-output
chroot $1 chown -R demo:demo /home/demo
chroot $1 chown -R demo:demo /home/demo/.mozilla
chroot $1 chown -R demo:demo /opt/OAIS
chroot $1 chown -R demo:demo /var/storeAIP

#Begin Qubit Configuration
chroot $1 /etc/init.d/mysql start
chroot $1 mysqladmin create qubit
cp scripts/php.ini $1/etc/php5/cli
cp scripts/php.ini $1/etc/php5/apache2
cp scripts/apache.default $1/etc/apache2/sites-available/default
chroot $1 apache2ctl restart
svn checkout http://qubit-toolkit.googlecode.com/svn/tags/release-1.0.8  qubit-svn
svn export qubit-svn $1/var/www/qubit

apache2ctl restart
chroot $1 chown -R www-data:www-data /var/www/qubit
chroot $1 sh -c 'echo EnableSendfile Off >> /etc/apache2/apache2.conf'
chroot $1 a2enmod rewrite

echo Apache is configured and Qubit has been downloaded please finish with the installer!
