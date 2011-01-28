sudo apt-get install libapache2-mod-wsgi python-django python-django-doc python-twisted python-pyinotify ffmpeg2theora libavcodec-unstripped-52 flashplugin-installer openjdk-6-jre openoffice.org openoffice.org-java-common libnotify-bin uuid httrack sendemail curl clamav incron nfs-common flac md5deep ffmpeg winff firebug imagemagick libapache2-mod-php5 mysql-server php5-cli php5-mysql php5-xsl subversion-tools par2 unrar p7zip-full python-execnet digikam kipi-plugins python-mysqldb nfs-kernel-server python-lxml inkscape dosfstools



version="`lsb_release -d | grep "Ubuntu 10.04"`"
if [ -n "$version" ]; 
	then
		##LUCID
		sudo add-apt-repository ppa:austin-arcintel/archivematica
	
	else
		##OTHERS
		sudo echo deb http://ppa.launchpad.net/austin-arcintel/archivematica/ubuntu lucid main >> /etc/apt/sources.list
		sudo echo deb-src http://ppa.launchpad.net/austin-arcintel/archivematica/ubuntu lucid main >> /etc/apt/sources.list 
fi
sudo apt-get update
sudo apt-get install bagit droid fits jhove # xena 

tmp="`pwd`"
svnDir=$(dirname $tmp)/
cd ./../buildVM/includes/
sudo ./vmInstaller-ica-atom.sh /.
sudo mv /etc/apache2/sites-available/default{,.dist}
sudo ln -s ${svnDir}buildVM/includes/apache.default /etc/apache2/sites-available/default
sudo /etc/init.d/apache2 restart
cd "$tmp"
