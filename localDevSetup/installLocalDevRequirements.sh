#!/bin/sh

# Install needed packages
sudo apt-get install \
  libapache2-mod-wsgi \
  python-pyinotify \
  ffmpeg2theora \
  libavcodec-unstripped-52 \
  flashplugin-installer \
  openjdk-6-jre \
  openoffice.org \
  openoffice.org-java-common \
  libnotify-bin \
  uuid \
  httrack \
  sendemail \
  curl \
  clamav \
  incron \
  nfs-common \
  flac \
  md5deep \
  ffmpeg \
  winff \
  firebug \
  imagemagick \
  libapache2-mod-php5 \
  mysql-server \
  php5-cli \
  php5-mysql \
  php5-xsl \
  subversion-tools \
  par2 \
  unrar \
  p7zip-full \
  python-execnet \
  digikam \
  kipi-plugins \
  python-mysqldb \
  nfs-kernel-server \
  python-lxml \
  inkscape \
  dosfstools \
  ufraw

# Get Ubuntu version installed
version="`lsb_release -d | grep "Ubuntu 10.04"`"

# Add extra repositories
if [ -n "$version" ]
  then
    # Lucid
    sudo add-apt-repository ppa:archivematica/externals-dev
    sudo add-apt-repository ppa:twisted-dev/ppa
  else
    # Others
    sudo echo deb http://ppa.launchpad.net/archivematica/externals-dev/ubuntu lucid main >> /etc/apt/sources.list
    sudo echo deb-src http://ppa.launchpad.net/archivematica/externals-dev/ubuntu lucid main >> /etc/apt/sources.list
fi

# Resynchronize package index from sources
sudo apt-get update

# Install extra packages
sudo apt-get install bagit droid fits jhove python-django python-twisted # xena

tmp="`pwd`"
svnDir=$(dirname $tmp)/
cd ./../buildVM/includes/

# Install ICA-AtoM and configure Apache
sudo ./vmInstaller-ica-atom.sh /.
sudo mv /etc/apache2/sites-available/default /etc/apache2/sites-available/default.dist
sudo ln -s ${svnDir}buildVM/includes/apache.default /etc/apache2/sites-available/default
sudo mv /var/www/index.html ./backup-index.html
sudo /etc/init.d/apache2 restart

cd "$tmp"
