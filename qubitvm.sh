#!/bin/bash
#Prepare Ubuntu
chroot $1 tar xvzf /usr/local/scripts.tar.gz
chroot $1 chmod -R 777 /etc/apt/sources.list
chroot $1 cp /etc/apt/sources.list /etc/apt/sources.list.bak
chroot $1 sed -i -e "s/# deb/deb/g" /etc/apt/sources.list
chroot $1 sed -i -e "s/localhost:9999/archive.ubuntu.com/g" /etc/apt/sources.list
chroot $1 sed -i -e "s/127.0.0.1:9999/archive.ubuntu.com/g" /etc/apt/sources.list
chroot $1 echo 'deb http://archive.ubuntu.com/ubuntu/ jaunty-proposed main restricted universe multiverse' >> /etc/apt/sources.list
chroot $1 aptitude update
chroot $1 aptitude -q -Ry build-dep -d openjdk-6-jre jacksum
chroot $1 aptitude --download-only install openjdk-6-jre jacksum 

#Install OAIS
chroot $1 mkdir /var/archivalstorage
cp -rf scripts/ingest $1/var/ingest
cp -rf scripts/OAIS $1/usr/local/OAIS
cp -rf scripts/.mozilla $1/home/qubitadmin/.mozilla
chroot $1 chmod -R 770 /home/qubitadmin/.mozilla
chroot $1 ln -s /var/archivalstorage/ /home/qubitadmin
chroot $1 ln -s /var/ingest/ /home/qubitadmin
chroot $1 mkdir -p /home/qubitadmin/Desktop
cp scripts/makeMD5 $1/home/qubitadmin/.gnome2/nautilus-scripts
cp scripts/checkMD5 $1/home/qubitadmin/.gnome2/nautilus-scripts
cp scripts/Qubit.png $1/usr/share/icons
cp scripts/ica-atom.desktop $1/home/qubitadmin/Desktop
cp scripts/droid.desktop $1/home/qubitadmin/Desktop
cp scripts/jhove.desktop $1/home/qubitadmin/Desktop
cp scripts/NLNZ-metadata-extractor.desktop $1/home/qubitadmin/Desktop
cp scripts/xena.desktop $1/home/qubitadmin/Desktop
cp scripts/rundroid.sh $1/usr/bin
cp scripts/runica.sh $1/usr/bin
cp scripts/runjhove.sh $1/usr/bin
cp scripts/runxena.sh $1/usr/bin
chroot $1 mkdir /home/qubitadmin/xena-output
chroot $1 chown -R qubitadmin:qubitadmin /home/qubitadmin
chroot $1 chown -R qubitadmin:qubitadmin /home/qubitadmin/.mozilla
chroot $1 chown -R qubitadmin:qubitadmin /usr/local/OAIS

#Begin Qubit Configuration
chroot $1 /etc/init.d/mysql start
chroot $1 mysqladmin create qubit
chroot $1 cp scripts/php.ini /etc/php5/cli
chroot $1 cp scripts/php.ini /etc/php5/apache2
chroot $1 cp scripts/apache.default /etc/apache2/sites-available/default
chroot $1 apache2ctl restart
chroot $1 svn checkout http://qubit-toolkit.googlecode.com/svn/trunk/ /var/www/qubit

apache2ctl restart
chroot $1 chown -R www-data:www-data /var/www/qubit
chroot $1 sh -c 'echo EnableSendfile Off >> /etc/apache2/apache2.conf'
chroot $1 a2enmod rewrite

#Cleanup
chroot $1 aptitude clean
chroot $1 passwd -e qubitadmin

echo Apache is configured and Qubit has been downloaded please finish with the installer!
